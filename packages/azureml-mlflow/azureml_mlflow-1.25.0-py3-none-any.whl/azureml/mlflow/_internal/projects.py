# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
The **AzureMLProjectBackend** module provides a class for executing MLflow projects using AzureML
and is based on the Mlflow Plugin documentation. The class consolidates information from an
Mlflow projects run and its AzureML tracking store to submit an AzureML ScriptRunConfig as an
Experiment Run.

The Submitted Run class provides a wrapper around an AzureML Run submitted from this class and
is a subclass of this Mlflow abstract class
https://github.com/mlflow/mlflow/blob/master/mlflow/projects/submitted_run.py
"""
import logging
import os

from mlflow.projects.backend.abstract_backend import AbstractBackend
from mlflow.tracking.client import MlflowClient
from mlflow.exceptions import ExecutionException
from mlflow.projects.utils import (fetch_and_validate_project, load_project)

# for Mlflow versions greater than 1.10.0, the implementation of a local backend
# moves functions we use to project utilities and creates a backend_config object for the
# user with default values like USE_CONDA, DOCKER_ARGS, etc.
# https://github.com/mlflow/mlflow/pull/3124
try:
    from mlflow.projects.utils import (get_entry_point_command, PROJECT_USE_CONDA)
except ImportError:
    from mlflow.projects import _get_entry_point_command as get_entry_point_command
    PROJECT_USE_CONDA = "USE_CONDA"

from azureml.exceptions import ExperimentExecutionException
from azureml.core.compute_target import ComputeTargetException
from azureml.core import Workspace, Experiment, ComputeTarget, ScriptRunConfig, Environment
from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml.mlflow._internal.submitted_run import AzureMLSubmittedRun
from azureml.mlflow._internal.store import AzureMLRestStore
from azureml.mlflow._internal.utils import VERSION_WARNING

from datetime import datetime

try:
    from azureml.mlflow._version import VERSION
except ImportError:
    VERSION = "0.0.0+dev"

_AZUREML_URI = "azureml://"
STREAM_OUTPUT = "STREAM_OUTPUT"
COMPUTE = "COMPUTE"
_LOCAL = "local"

_logger = logging.getLogger(__name__)
_CONSOLE_MSG = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " INFO azureml.mlflow: === {} ==="


def _load_azure_workspace():
    '''
    Load existing Azure Workspace from Tracking Store
    :rtype: AzureML Workspace object
    '''
    try:
        def_store = MlflowClient()._tracking_client.store
    except ExecutionException:
        _logger.warning(VERSION_WARNING.format("MlflowClient()._tracking_client.store"))
        def_store = MlflowClient().store
    if isinstance(def_store, AzureMLRestStore):
        workspace = Workspace(def_store.service_context.subscription_id,
                              def_store.service_context.resource_group_name,
                              def_store.service_context.workspace_name,
                              auth=def_store.service_context.get_auth())
        return workspace
    else:
        raise ExecutionException("Workspace not found, please set the tracking URI in your script to AzureML.")


def _load_azure_experiment(workspace, experiment_id):
    ''' Experiment name is registered by MLflow from the script and is
    referenced by its ID, which we can use to retrieve the experiment name.
    :param workspace: AzureML Workspace object
    :param experiment_id: MLflow experiment ID
    :return experiment: AzureML Experiment object
    '''
    experiment_name = MlflowClient().get_experiment(experiment_id).name
    try:
        experiment = Experiment(workspace=workspace, name=experiment_name)
        _logger.info(_CONSOLE_MSG.format("Experiment {} found.".format(experiment_name)))
    except ExperimentExecutionException as e:
        raise ExecutionException("Mlflow Experiment name not found. /n{}".format(e))
    return experiment


def _load_remote_environment(mlproject):
    '''
    Returns Environment object for remote compute execution with conda
    :param mlproject: instance of Project object from mlflow.projects._project_spec
    :return environment: AzureML Environment object
    '''
    if mlproject.conda_env_path:
        _logger.info(_CONSOLE_MSG.format("Creating remote conda environment for project using MLproject"))
        environment = Environment.from_conda_specification(name="environment", file_path=mlproject.conda_env_path)
        if environment.python.conda_dependencies._get_pip_package_with_prefix("azureml-mlflow") == []:
            _logger.warning("WARNING: MLproject doesn't contain pip dependency azureml-mlflow. Adding it now...")
            environment.python.conda_dependencies.add_pip_package("azureml-mlflow")
        environment.docker.enabled = True
        return environment
    elif mlproject.docker_env:
        '''Docker support is WIP!'''
        raise ExecutionException("Docker support is in progress, please specify a conda environment instead")


def _load_local_environment(mlproject, use_conda):
    '''
    Returns Environment object for project execution on local compute.
    If the MLproject contains a conda environment specification and use_conda is True
    from the backend_config object, we create a new environment from that specification
    for project training.
    If use_conda is False, we use the local, activated conda environment.
    :param mlproject: Project object loaded by Mlflow
    :param use_conda: bool
    :rtype environment: AzureML Environment object
    '''
    if mlproject.docker_env:
        '''Docker support is WIP!'''
        raise ExecutionException("Docker support is in progress, please specify a conda environment instead")
    elif use_conda is True and mlproject.conda_env_path:
        print(_CONSOLE_MSG.format("Creating conda environment from Mlproject for local run"))
        try:
            environment = Environment.from_conda_specification(name="environment", file_path=mlproject.conda_env_path)
            environment.python.user_managed_dependencies = False
            # check if azureml-mlflow in pip dependencies
            if environment.python.conda_dependencies._get_pip_package_with_prefix("azureml-mlflow") == []:
                _logger.warning("WARNING: MLproject doesn't contain pip dependency azureml-mlflow. Adding it now...")
                environment.python.conda_dependencies.add_pip_package("azureml-mlflow")
        except ExecutionException as e:
            raise ExecutionException(e)
        return environment
    else:
        conda_home = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_home:
            try:
                if conda_home == "base":
                    _logger.warning("WARNING: Using inactive base conda environement for local run")
                environment = Environment.from_existing_conda_environment("environment", conda_home)
                environment.python.user_managed_dependencies = True
                print(_CONSOLE_MSG.format("Using local conda environment {} for local run".format(conda_home)))
            except ExecutionException as e:
                raise ExecutionException(e)
            return environment
        else:
            raise ExecutionException("Local conda environment not found, check your path.")


def _load_compute_target(workspace, backend_config):
    '''
    Returns the ComputeTarget object for associated with user's workspace and the
    name of the target compute
    :param workspace: AzureML Workspace object
    :param backend_config: dictionary containing target compute name
    :return ComputeTarget: AzureML ComputeTarget object
    '''
    target_name = backend_config[COMPUTE]
    try:
        compute = ComputeTarget(workspace=workspace, name=target_name)
        # pylint: disable = abstract-class-instantiated
        _logger.info(_CONSOLE_MSG.format("Found existing cluster {}, using it.".format(target_name)))
    except ComputeTargetException as e:
        raise ComputeTargetException(e)
    return compute


@experimental
class AzureMLProjectBackend(AbstractBackend):
    '''
    Resolves MLflow projects to be submitted using AzureML on local compute or remotely on
    AML Compute and RemoteVM.
    '''
    def run(self, project_uri, entry_point, params,
            version, backend_config, tracking_uri, experiment_id):
        # doing this handling bc positional argument fix not in mlflow <= 1.10.0 release
        # https://github.com/mlflow/mlflow/issues/3138
        if _AZUREML_URI not in tracking_uri and _AZUREML_URI in experiment_id:
            tracking_uri, experiment_id = experiment_id, tracking_uri

        # use_conda value from mlflow.project.run call propagated to backend_config
        # release after 1.10.0, so if use_conda key not in backend config, assume to be True
        # if the user hasn't passed a backend_config and has set backend="azureml", assume
        # that it's a local run using local conda environment (i.e. use_conda = False)
        if backend_config is None:
            backend_config = {PROJECT_USE_CONDA: False}
        elif PROJECT_USE_CONDA not in backend_config:
            backend_config[PROJECT_USE_CONDA] = True
        use_conda = backend_config[PROJECT_USE_CONDA]
        stream_output = backend_config[STREAM_OUTPUT] if STREAM_OUTPUT in backend_config else True
        compute = backend_config[COMPUTE] if COMPUTE in backend_config else None

        try:
            work_dir = fetch_and_validate_project(project_uri, version, entry_point, params)
            mlproject = load_project(work_dir)
        except ExecutionException as e:
            raise ExecutionException(e)
        # process mlflow parameters into a format usable for AzureML ScriptRunConfig
        command_args = []
        command_args += get_entry_point_command(mlproject, entry_point, params, None)

        # components for launching an AzureML ScriptRun
        workspace = _load_azure_workspace()
        experiment = _load_azure_experiment(workspace, experiment_id)

        # TODO: mlflow system tag mlflow.source.name is null after the switch from script, args to command
        src = ScriptRunConfig(source_directory=work_dir, command=command_args)

        # in case customer sets target to local
        if compute and compute != _LOCAL and compute != _LOCAL.upper():
            remote_environment = _load_remote_environment(mlproject)
            registered_env = remote_environment.register(workspace=workspace)
            cpu_cluster = _load_compute_target(workspace, backend_config)
            src.run_config.target = cpu_cluster.name
            src.run_config.environment = registered_env
        else:
            local_environment = _load_local_environment(mlproject, use_conda)
            src.run_config.environment = local_environment
        submitted_run = experiment.submit(config=src)
        _logger.info(_CONSOLE_MSG.format("AzureML-Mlflow {} Experiment submitted".format(experiment.name)))
        return AzureMLSubmittedRun(submitted_run, stream_output)
