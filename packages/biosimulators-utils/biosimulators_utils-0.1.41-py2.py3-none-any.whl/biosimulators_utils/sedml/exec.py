""" Utilities for executing tasks in SED documents

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2020-12-06
:Copyright: 2020, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ..config import get_config, Colors
from ..log.data_model import Status, SedDocumentLog, TaskLog, ReportLog, Plot2DLog, Plot3DLog  # noqa: F401
from ..log.utils import init_sed_document_log, StandardOutputErrorCapturer
from ..plot.data_model import PlotFormat
from ..plot.io import write_plot_2d, write_plot_3d
from ..report.data_model import VariableResults, DataSetResults, ReportResults, ReportFormat  # noqa: F401
from ..report.io import ReportWriter
from ..utils.core import pad_arrays_to_consistent_shapes
from ..warnings import warn
from .data_model import SedDocument, Model, Task, RepeatedTask, Report, Plot2D, Plot3D, ModelAttributeChange
from .exceptions import SedmlExecutionError
from .io import SedmlSimulationReader
from .utils import (resolve_model_and_apply_xml_changes, get_variables_for_task,
                    calc_data_generators_results, resolve_range, get_models_referenced_by_task,
                    get_value_of_variable_model_xml_targets, calc_compute_model_change_new_value,
                    apply_changes_to_xml_model, get_first_last_models_executed_by_task)
from .warnings import NoTasksWarning, NoOutputsWarning, SedmlFeatureNotSupportedWarning
from lxml import etree  # noqa: F401
import copy
import datetime
import numpy
import os
import sys
import tempfile
import termcolor
import types  # noqa: F401


__all__ = [
    'exec_sed_doc',
    'exec_task',
    'exec_repeated_task',
    'exec_report',
    'exec_plot_2d',
    'exec_plot_3d',
]


def exec_sed_doc(task_executer, doc, working_dir, base_out_path, rel_out_path=None,
                 apply_xml_model_changes=False, report_formats=None, plot_formats=None,
                 log=None, indent=0, pretty_print_modified_xml_models=False):
    """ Execute the tasks specified in a SED document and generate the specified outputs

    Args:
        task_executer (:obj:`types.FunctionType`): function to execute each task in the SED-ML file.
            The function must implement the following interface::

                def exec_task(task, variables, log=None):
                    ''' Execute a simulation and return its results

                    Args:
                       task (:obj:`Task`): task
                       variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
                       log (:obj:`TaskLog`, optional): log for the task

                    Returns:
                       :obj:`VariableResults`: results of variables
                    '''
                    pass

        doc (:obj:`SedDocument` or :obj:`str`): SED document or a path to SED-ML file which defines a SED document
        working_dir (:obj:`str`): working directory of the SED document (path relative to which models are located)

        base_out_path (:obj:`str`): path to store the outputs

            * CSV: directory in which to save outputs to files
              ``{base_out_path}/{rel_out_path}/{report.id}.csv``
            * HDF5: directory in which to save a single HDF5 file (``{base_out_path}/reports.h5``),
              with reports at keys ``{rel_out_path}/{report.id}`` within the HDF5 file

        rel_out_path (:obj:`str`, optional): path relative to :obj:`base_out_path` to store the outputs
        apply_xml_model_changes (:obj:`bool`, optional): if :obj:`True`, apply any model changes specified in the SED-ML file before
            calling :obj:`task_executer`.
        report_formats (:obj:`list` of :obj:`ReportFormat`, optional): report format (e.g., csv or h5)
        plot_formats (:obj:`list` of :obj:`PlotFormat`, optional): plot format (e.g., pdf)
        log (:obj:`SedDocumentLog`, optional): log of the document
        indent (:obj:`int`, optional): degree to indent status messages
        pretty_print_modified_xml_models (:obj:`bool`, optional): if :obj:`True`, pretty print modified XML models

    Returns:
        :obj:`tuple`:

            * :obj:`ReportResults`: results of each report
            * :obj:`SedDocumentLog`: log of the document
    """
    config = get_config()

    # process arguments
    if not isinstance(doc, SedDocument):
        doc = SedmlSimulationReader().run(doc)
    else:
        doc = copy.deepcopy(doc)

    if report_formats is None:
        report_formats = [ReportFormat(format_value) for format_value in config.REPORT_FORMATS]

    if plot_formats is None:
        plot_formats = [PlotFormat(format_value) for format_value in config.PLOT_FORMATS]

    log = log or init_sed_document_log(doc)

    verbose = config.VERBOSE

    # update status
    exceptions = []

    # execute tasks
    if not doc.tasks:
        warn('SED document does not describe any tasks.', NoTasksWarning)

    # TODO: initialize reports with their eventual shapes; this requires individual simulation tools to pass
    # information about the shape of their output to this method
    variable_results = VariableResults()
    report_results = ReportResults()

    print('{}Found {} tasks and {} outputs:\n{}Tasks:\n{}{}\n{}Outputs:\n{}{}'.format(
        ' ' * 2 * indent,
        len(doc.tasks),
        len(doc.outputs),
        ' ' * 2 * (indent + 1),
        ' ' * 2 * (indent + 2),
        ('\n' + ' ' * 2 * (indent + 2)).join(sorted('`' + task.id + '`' for task in doc.tasks)),
        ' ' * 2 * (indent + 1),
        ' ' * 2 * (indent + 2),
        ('\n' + ' ' * 2 * (indent + 2)).join(sorted('`' + output.id + '`' for output in doc.outputs)),
    ))
    for i_task, task in enumerate(doc.tasks):
        print('{}Executing task {}: `{}`'.format(' ' * 2 * indent, i_task + 1, task.id))

        task_log = log.tasks[task.id]
        task_log.status = Status.RUNNING
        task_log.export()

        # Execute task
        print('{}Executing simulation ...'.format(' ' * 2 * (indent + 1)), end='')
        sys.stdout.flush()
        with StandardOutputErrorCapturer(relay=verbose) as captured:
            start_time = datetime.datetime.now()
            try:
                # get model and apply changes
                original_models = get_models_referenced_by_task(task)
                original_model_sources = {}
                original_model_changes = {}
                temp_model_sources = []
                model_etrees = {}
                for original_model in original_models:
                    original_model_sources[original_model.id] = original_model.source
                    original_model_changes[original_model.id] = original_model.changes

                    temp_model, temp_model_source, model_etree = resolve_model_and_apply_xml_changes(
                        original_model, doc, working_dir,
                        apply_xml_model_changes=apply_xml_model_changes,
                        pretty_print_modified_xml_models=pretty_print_modified_xml_models)

                    original_model.source = temp_model.source
                    original_model.changes = temp_model.changes

                    if temp_model_source:
                        temp_model_sources.append(temp_model_source)

                    model_etrees[original_model.id] = model_etree

                task_vars = get_variables_for_task(doc, task)

                # execute task
                if isinstance(task, Task):
                    task_var_results = exec_task(task, task_executer, task_vars, doc, log=task_log)

                elif isinstance(task, RepeatedTask):
                    task_var_results = exec_repeated_task(task, task_executer, task_vars, doc,
                                                          apply_xml_model_changes=apply_xml_model_changes,
                                                          model_etrees=model_etrees,
                                                          pretty_print_modified_xml_models=pretty_print_modified_xml_models)

                else:  # pragma: no cover: already validated by :obj:`get_models_referenced_by_task`
                    raise NotImplementedError('Tasks of type {} are not supported.'.format(task.__class__.__name__))

                # append results
                for key, value in task_var_results.items():
                    variable_results[key] = value

                # log status
                task_status = Status.SUCCEEDED
                task_exception = None

                # cleanup modified model sources
                for temp_model_source in temp_model_sources:
                    os.remove(temp_model_source)
                for original_model in original_models:
                    original_model.source = original_model_sources[original_model.id]
                    original_model.changes = original_model_changes[original_model.id]
            except Exception as exception:
                exceptions.append(exception)
                task_status = Status.FAILED
                task_exception = exception

        if task_log:
            task_log.status = task_status
            task_log.exception = task_exception
            task_log.output = captured.get_text()
            task_log.duration = (datetime.datetime.now() - start_time).total_seconds()
            task_log.export()
        print(' ' + termcolor.colored(task_status.value.lower(), Colors[task_status.value.lower()].value))

        # generate outputs
        print('{}Generating {} outputs ...'.format(' ' * 2 * (indent + 1), len(doc.outputs)))
        task_contributes_to_output = False
        for i_output, output in enumerate(doc.outputs):
            print('{}Generating output {}: `{}` ...'.format(' ' * 2 * (indent + 2), i_output + 1, output.id), end='')
            sys.stdout.flush()
            start_time = datetime.datetime.now()
            with StandardOutputErrorCapturer(relay=verbose) as captured:
                try:
                    if log.outputs[output.id].status == Status.SUCCEEDED:
                        output_status = log.outputs[output.id].status
                        print(' ' + termcolor.colored(output_status.value.lower(), Colors[output_status.value.lower()].value))
                        continue

                    if isinstance(output, Report):
                        report_results[output.id], output_status, output_exception, task_contributes_to_report = exec_report(
                            output, variable_results,
                            base_out_path, rel_out_path, report_formats,
                            task,
                            log.outputs[output.id])
                        task_contributes_to_output = task_contributes_to_output or task_contributes_to_report

                    elif isinstance(output, Plot2D):
                        output_status, output_exception, task_contributes_to_plot = exec_plot_2d(
                            output, variable_results,
                            base_out_path, rel_out_path, plot_formats,
                            task,
                            log.outputs[output.id])
                        task_contributes_to_output = task_contributes_to_output or task_contributes_to_plot

                    elif isinstance(output, Plot3D):
                        output_status, output_exception, task_contributes_to_plot = exec_plot_3d(
                            output, variable_results,
                            base_out_path, rel_out_path, plot_formats,
                            task,
                            log.outputs[output.id])
                        task_contributes_to_output = task_contributes_to_output or task_contributes_to_plot

                    else:
                        # unreachable because the above cases cover all types of outputs
                        raise NotImplementedError('Outputs of type {} are not supported.'.format(output.__class__.__name__))

                except Exception as exception:
                    output_status = Status.FAILED
                    output_exception = exception

            log.outputs[output.id].status = output_status
            log.outputs[output.id].exception = output_exception
            log.outputs[output.id].output = captured.get_text()
            log.outputs[output.id].duration = (datetime.datetime.now() - start_time).total_seconds()
            log.outputs[output.id].export()

            if output_exception:
                exceptions.append(output_exception)

            print(' ' + termcolor.colored(output_status.value.lower(), Colors[output_status.value.lower()].value))

        if not task_contributes_to_output:
            warn('Task {} does not contribute to any outputs.'.format(task.id), NoOutputsWarning)

    # finalize the status of the outputs
    for output_log in log.outputs.values():
        output_log.finalize()

    # summarize execution
    task_status_count = {
        Status.SUCCEEDED: 0,
        Status.SKIPPED: 0,
        Status.FAILED: 0,
    }
    for task_log in log.tasks.values():
        task_status_count[task_log.status] += 1

    output_status_count = {
        Status.SUCCEEDED: 0,
        Status.SKIPPED: 0,
        Status.FAILED: 0,
    }
    for output_log in log.outputs.values():
        output_status_count[output_log.status] += 1

    print('')
    print('{}Executed {} tasks and {} outputs:'.format(' ' * 2 * indent, len(doc.tasks), len(doc.outputs)))
    print('{}  Tasks:'.format(' ' * 2 * indent))
    print('{}    Succeeded: {}'.format(' ' * 2 * indent, task_status_count[Status.SUCCEEDED]))
    print('{}    Skipped: {}'.format(' ' * 2 * indent, task_status_count[Status.SKIPPED]))
    print('{}    Failed: {}'.format(' ' * 2 * indent, task_status_count[Status.FAILED]))
    print('{}  Outputs:'.format(' ' * 2 * indent))
    print('{}    Succeeded: {}'.format(' ' * 2 * indent, output_status_count[Status.SUCCEEDED]))
    print('{}    Skipped: {}'.format(' ' * 2 * indent, output_status_count[Status.SKIPPED]))
    print('{}    Failed: {}'.format(' ' * 2 * indent, output_status_count[Status.FAILED]))

    # raise exceptions
    if exceptions:
        msg = 'The SED document did not execute successfully:\n\n  {}'.format(
            '\n\n  '.join(str(exceptions).replace('\n', '\n  ') for exceptions in exceptions))
        raise SedmlExecutionError(msg)

    # return the results of the reports
    return report_results, log


def exec_task(task, task_executer, task_vars, doc, log=None):
    """ Execute a basic SED task

    Args:
        task (:obj:`Task`): task
        task_executer (:obj:`types.FunctionType`): function to execute each task in the SED-ML file.
            The function must implement the following interface::

                def exec_task(task, variables, log=None):
                    ''' Execute a simulation and return its results

                    Args:
                        task (:obj:`Task`): task
                        variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
                        log (:obj:`TaskLog`, optional): log for the task

                    Returns:
                        :obj:`tuple`:

                            * :obj:`VariableResults`: results of variables
                            * :obj:`TaskLog`: log
                    '''
                    pass

        task_vars (:obj:`list` of :obj:`Variable`): variables that task must record
        doc (:obj:`SedDocument` or :obj:`str`): SED document or a path to SED-ML file which defines a SED document
        log (:obj:`TaskLog`, optional): log

    Returns:
        :obj:`VariableResults`: results of the variables
    """
    # execute task
    task_variable_results, _ = task_executer(task, task_vars, log=log)

    # check that the expected variables were recorded
    variable_results = VariableResults()
    for var in task_vars:
        variable_results[var.id] = task_variable_results.get(var.id, None)

    # return results
    return variable_results


def exec_repeated_task(task, task_executer, task_vars, doc, apply_xml_model_changes=False, model_etrees=None,
                       pretty_print_modified_xml_models=False):
    """ Execute a repeated SED task

    Args:
        task (:obj:`RepeatedTask`): task
        task_executer (:obj:`types.FunctionType`): function to execute each task in the SED-ML file.
            The function must implement the following interface::

                def exec_task(task, variables, log=None):
                    ''' Execute a simulation and return its results

                    Args:
                       task (:obj:`Task`): task
                       variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
                       log (:obj:`TaskLog`, optional): log for the task

                    Returns:
                       :obj:`VariableResults`: results of variables
                    '''
                    pass

        task_vars (:obj:`list` of :obj:`Variable`): variables that task must record
        doc (:obj:`SedDocument` or :obj:`str`): SED document or a path to SED-ML file which defines a SED document
        apply_xml_model_changes (:obj:`bool`, optional): if :obj:`True`, apply any model changes specified in the SED-ML file before
            calling :obj:`task_executer`.
        model_etrees (:obj:`dict` of :obj:`str` to :obj:`etree._Element`)
        pretty_print_modified_xml_models (:obj:`bool`, optional): if :obj:`True`, pretty print modified XML models

    Returns:
        :obj:`VariableResults`: results of the variables
    """
    # warn about inability to not reset models
    if not task.reset_model_for_each_iteration:
        models = get_first_last_models_executed_by_task(task)
        if models[0] == models[-1]:
            msg = (
                'Only independent execution of iterations of repeated tasks is supported. '
                'Successive iterations will not be executed starting from the end state of the previous iteration.'
            )
            warn(msg, SedmlFeatureNotSupportedWarning)

    sub_tasks = sorted(task.sub_tasks, key=lambda sub_task: sub_task.order)
    for prev_sub_task, next_sub_task in zip(sub_tasks[0:-1], sub_tasks[1:]):
        if get_first_last_models_executed_by_task(prev_sub_task.task)[-1] == get_first_last_models_executed_by_task(next_sub_task.task)[0]:
            msg = (
                'Only independent execution of sub-tasks is supported. '
                'Successive sub-tasks will not be executed starting from the end state of the previous sub-task.'
            )
            warn(msg, SedmlFeatureNotSupportedWarning)
            break

    # hold onto model to be able to reset it
    if task.reset_model_for_each_iteration:
        original_doc = doc
        original_task = task
        original_model_etrees = model_etrees

    # resolve the ranges
    main_range_values = resolve_range(task.range, model_etrees=model_etrees)

    range_values = {}
    for range in task.ranges:
        range_values[range.id] = resolve_range(range, model_etrees=model_etrees)
    for change in task.changes:
        if change.range:
            range_values[change.range.id] = resolve_range(change.range, model_etrees=model_etrees)

    # initialize the results of the sub-tasks
    variable_results = VariableResults()
    for var in task_vars:
        variable_results[var.id] = []
        for main_range_value in main_range_values:
            variable_results[var.id].append([None] * len(task.sub_tasks))

    # iterate over the main range, apply the changes to the model(s), execute the sub-tasks, and record the results of the tasks
    for i_main_range, _ in enumerate(main_range_values):
        # reset the models referenced by the task
        if task.reset_model_for_each_iteration:
            doc = copy.deepcopy(original_doc)
            task = next(task for task in doc.tasks if task.id == original_task.id)
            model_etrees = copy.deepcopy(original_model_etrees)

        # get range values
        current_range_values = {}
        current_range_values[task.range.id] = range_values[task.range.id][i_main_range]
        for range in task.ranges:
            current_range_values[range.id] = range_values[range.id][i_main_range]
        for change in task.changes:
            if change.range:
                current_range_values[change.range.id] = range_values[change.range.id][i_main_range]

        # apply the changes to the models
        for change in task.changes:
            variable_values = {}
            for variable in change.variables:
                if not apply_xml_model_changes:
                    raise NotImplementedError('Set value changes that involve variables of non-XML-encoded models are not supported.')
                variable_values[variable.id] = get_value_of_variable_model_xml_targets(variable, model_etrees)

            new_value = calc_compute_model_change_new_value(change, variable_values=variable_values, range_values=current_range_values)
            if new_value == int(new_value):
                new_value = str(int(new_value))
            else:
                new_value = str(new_value)

            if change.symbol:
                raise NotImplementedError('Set value changes of symbols is not supported.')

            attr_change = ModelAttributeChange(target=change.target, target_namespaces=change.target_namespaces, new_value=new_value)

            if apply_xml_model_changes:
                model = Model(changes=[attr_change])
                apply_changes_to_xml_model(model, model_etrees[change.model.id], None, None)

            else:
                change.model.changes.append(attr_change)

        # sort the sub-tasks
        sub_tasks = sorted(task.sub_tasks, key=lambda sub_task: sub_task.order)

        # execute the sub-tasks and record their results
        for i_sub_task, sub_task in enumerate(sub_tasks):
            if isinstance(sub_task.task, Task):
                if apply_xml_model_changes:
                    model = sub_task.task.model
                    original_model_source = model.source
                    fid, model.source = tempfile.mkstemp(suffix='.xml')
                    os.close(fid)

                    model_etrees[model.id].write(model.source,
                                                 xml_declaration=True,
                                                 encoding="utf-8",
                                                 standalone=False,
                                                 pretty_print=pretty_print_modified_xml_models)

                sub_task_var_results = exec_task(sub_task.task, task_executer, task_vars, doc)

                if apply_xml_model_changes:
                    os.remove(model.source)
                    model.source = original_model_source

            elif isinstance(sub_task.task, RepeatedTask):
                sub_task_var_results = exec_repeated_task(sub_task.task, task_executer, task_vars, doc,
                                                          apply_xml_model_changes=apply_xml_model_changes,
                                                          model_etrees=model_etrees,
                                                          pretty_print_modified_xml_models=pretty_print_modified_xml_models)

            else:  # pragma: no cover: already validated by :obj:`get_first_last_models_executed_by_task`
                raise NotImplementedError('Tasks of type {} are not supported.'.format(sub_task.task.__class__.__name__))

            for var in task_vars:
                variable_results[var.id][i_main_range][i_sub_task] = sub_task_var_results.get(var.id, None)

    # shape results to consistent size
    arrays = []
    for var in task_vars:
        for i_main_range, _ in enumerate(main_range_values):
            for i_sub_task, sub_task in enumerate(sub_tasks):
                arrays.append(variable_results[var.id][i_main_range][i_sub_task])

    padded_arrays = pad_arrays_to_consistent_shapes(arrays)

    i_array = 0
    for var in task_vars:
        for i_main_range, _ in enumerate(main_range_values):
            for i_sub_task, sub_task in enumerate(sub_tasks):
                variable_results[var.id][i_main_range][i_sub_task] = padded_arrays[i_array]
                i_array += 1

        variable_results[var.id] = numpy.array(variable_results[var.id])

    # return the results of the task
    return variable_results


def exec_report(report, variable_results, base_out_path, rel_out_path, formats, task, log):
    """ Execute a report, generating the data sets which are available

    Args:
        report (:obj:`Report`): report
        variable_results (:obj:`VariableResults`): result of each data generator
        base_out_path (:obj:`str`): path to store the outputs

            * CSV: directory in which to save outputs to files
              ``{base_out_path}/{rel_out_path}/{report.id}.csv``
            * HDF5: directory in which to save a single HDF5 file (``{base_out_path}/reports.h5``),
              with reports at keys ``{rel_out_path}/{report.id}`` within the HDF5 file

        rel_out_path (:obj:`str`, optional): path relative to :obj:`base_out_path` to store the outputs
        formats (:obj:`list` of :obj:`ReportFormat`, optional): report format (e.g., csv or h5)
        task (:obj:`Task`): task
        log (:obj:`ReportLog`, optional): log of report

    Returns:
        :obj:`tuple`:

            * :obj:`DataSetResults`: report
            * :obj:`Status`: status
            * :obj:`Exception`: exception for failure
            * :obj:`bool`: whether :obj:`task` contribute a variable to the report
    """
    # calculate data generators
    data_generators = set()
    for data_set in report.data_sets:
        data_generators.add(data_set.data_generator)

    data_gen_results, data_gen_statuses, data_gen_exceptions, task_contributes_to_report = calc_data_generators_results(
        data_generators, variable_results, report, task, make_shapes_consistent=False)

    # collect data sets
    data_set_results = {}

    running = False
    succeeded = True
    failed = False

    for data_set in report.data_sets:
        data_gen_res = data_gen_results[data_set.data_generator.id]
        data_set_results[data_set.id] = data_gen_res

        data_gen_status = data_gen_statuses[data_set.data_generator.id]
        log.data_sets[data_set.id] = data_gen_status
        if data_gen_status == Status.FAILED:
            failed = True
        if data_gen_status == Status.SUCCEEDED:
            running = True
        else:
            succeeded = False

    for format in formats:
        ReportWriter().run(report,
                           data_set_results,
                           base_out_path,
                           os.path.join(rel_out_path, report.id) if rel_out_path else report.id,
                           format=format)

    if failed:
        status = Status.FAILED

    elif running:
        if succeeded:
            status = Status.SUCCEEDED
        else:
            status = Status.RUNNING

    else:
        status = Status.QUEUED

    return data_set_results, status, data_gen_exceptions, task_contributes_to_report


def exec_plot_2d(plot, variable_results, base_out_path, rel_out_path, formats, task, log):
    """ Execute a 2D plot, generating the curves which are available

    Args:
        plot (:obj:`Plot2D`): plot
        variable_results (:obj:`VariableResults`): result of each data generator
        base_out_path (:obj:`str`): base path to store the plot. Complete path is
            ``{base_out_path}/{rel_out_path}/{plot.id}.csv``
        rel_out_path (:obj:`str`, optional): path relative to :obj:`base_out_path` to store the plot
        formats (:obj:`list` of :obj:`PlotFormat`, optional): plot format (e.g., pdf)
        task (:obj:`Task`): task
        log (:obj:`ReportLog`, optional): log of plot

    Returns:
        :obj:`tuple`:

            * :obj:`Status`: status
            * :obj:`Exception`: exception for failure
            * :obj:`bool`: whether :obj:`task` contributes a variable to the plot
    """
    # calculate data generators
    data_generators = set()
    for curve in plot.curves:
        data_generators.add(curve.x_data_generator)
        data_generators.add(curve.y_data_generator)

    data_gen_results, data_gen_statuses, data_gen_exceptions, task_contributes_to_plot = calc_data_generators_results(
        data_generators, variable_results, plot, task)

    # collect data sets
    running = False
    succeeded = True
    failed = False

    succeeded_curves = []
    for curve in plot.curves:
        x_data_gen_status = data_gen_statuses[curve.x_data_generator.id]
        y_data_gen_status = data_gen_statuses[curve.y_data_generator.id]

        if x_data_gen_status == Status.SUCCEEDED and y_data_gen_status == Status.SUCCEEDED:
            curve_status = Status.SUCCEEDED
            succeeded_curves.append(curve)
        elif x_data_gen_status == Status.FAILED or y_data_gen_status == Status.FAILED:
            curve_status = Status.FAILED
        else:
            curve_status = Status.QUEUED

        log.curves[curve.id] = curve_status

        if curve_status == Status.FAILED:
            failed = True
        if curve_status == Status.SUCCEEDED:
            running = True
        else:
            succeeded = False

    for format in formats:
        write_plot_2d(Plot2D(curves=succeeded_curves),
                      data_gen_results,
                      base_out_path,
                      os.path.join(rel_out_path, plot.id) if rel_out_path else plot.id,
                      format=format)

    # determine the overall status of the plot
    if failed:
        status = Status.FAILED

    elif running:
        if succeeded:
            status = Status.SUCCEEDED
        else:
            status = Status.RUNNING

    else:
        status = Status.QUEUED

    # return
    return status, data_gen_exceptions, task_contributes_to_plot


def exec_plot_3d(plot, variable_results, base_out_path, rel_out_path, formats, task, log):
    """ Execute a 3D plot, generating the surfaces which are available

    Args:
        plot (:obj:`Plot3D`): plot
        variable_results (:obj:`VariableResults`): result of each data generator
        base_out_path (:obj:`str`): base path to store the plot. Complete path is
          ``{base_out_path}/{rel_out_path}/{plot.id}.pdf``
        rel_out_path (:obj:`str`, optional): path relative to :obj:`base_out_path` to store the plot
        formats (:obj:`list` of :obj:`PlotFormat`, optional): plot format (e.g., pdf)
        task (:obj:`Task`): task
        log (:obj:`ReportLog`, optional): log of plot

    Returns:
        :obj:`tuple`:

            * :obj:`Status`: status
            * :obj:`Exception`: exception for failure
            * :obj:`bool`: whether :obj:`task` contributes a variable to the plot
    """
    # calculate data generators
    data_generators = set()
    for surface in plot.surfaces:
        data_generators.add(surface.x_data_generator)
        data_generators.add(surface.y_data_generator)
        data_generators.add(surface.z_data_generator)

    data_gen_results, data_gen_statuses, data_gen_exceptions, task_contributes_to_plot = calc_data_generators_results(
        data_generators, variable_results, plot, task)

    # collect data sets
    running = False
    succeeded = True
    failed = False

    succeeded_surfaces = []
    for surface in plot.surfaces:
        x_data_gen_status = data_gen_statuses[surface.x_data_generator.id]
        y_data_gen_status = data_gen_statuses[surface.y_data_generator.id]
        z_data_gen_status = data_gen_statuses[surface.z_data_generator.id]

        if x_data_gen_status == Status.SUCCEEDED and y_data_gen_status == Status.SUCCEEDED and z_data_gen_status == Status.SUCCEEDED:
            surface_status = Status.SUCCEEDED
            succeeded_surfaces.append(surface)
        elif x_data_gen_status == Status.FAILED or y_data_gen_status == Status.FAILED or z_data_gen_status == Status.FAILED:
            surface_status = Status.FAILED
        else:
            surface_status = Status.QUEUED

        log.surfaces[surface.id] = surface_status

        if surface_status == Status.FAILED:
            failed = True
        if surface_status == Status.SUCCEEDED:
            running = True
        else:
            succeeded = False

    for format in formats:
        write_plot_3d(Plot3D(surfaces=succeeded_surfaces),
                      data_gen_results,
                      base_out_path,
                      os.path.join(rel_out_path, plot.id) if rel_out_path else plot.id,
                      format=format)

    # determine the overall status of the plot
    if failed:
        status = Status.FAILED

    elif running:
        if succeeded:
            status = Status.SUCCEEDED
        else:
            status = Status.RUNNING

    else:
        status = Status.QUEUED

    # return
    return status, data_gen_exceptions, task_contributes_to_plot
