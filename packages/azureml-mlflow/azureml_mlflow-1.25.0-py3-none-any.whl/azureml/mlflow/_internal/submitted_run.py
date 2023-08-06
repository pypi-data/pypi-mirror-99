# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

'''
The Submitted Run class provides a wrapper around an AzureML Run submitted
from azureml_projects_run class and is a subclass of this Mlflow abstract class
https://github.com/mlflow/mlflow/blob/master/mlflow/projects/submitted_run.py
'''
import logging
from six import raise_from

from mlflow.projects.submitted_run import SubmittedRun

from azureml.exceptions import RunEnvironmentException, ExperimentExecutionException, ActivityFailedException
from azureml._base_sdk_common._docstring_wrapper import experimental

_logger = logging.getLogger(__name__)


@experimental
class AzureMLSubmittedRun(SubmittedRun):
    '''
    Instance of SubmittedRun corresponding to an azureml.core Run
    launched to run an MLflow project. SubmittedRun is a wrapper
    around a Run and exposes methods for waiting on
    and cancelling the run.
    '''
    def __init__(self, run, stream_output):
        super(AzureMLSubmittedRun, self).__init__()
        self._run = run
        self._run_id = run.id
        self._stream_output = stream_output

    @property
    def run_id(self):
        return self._run_id

    def wait(self):
        try:
            self._run.wait_for_completion(show_output=self._stream_output, wait_post_processing=True)
        except (ExperimentExecutionException, ActivityFailedException) as e:
            _logger.warning("Submitted Run failed with exception {}".format(e))
        return self.get_status() == "Completed"

    def get_status(self):
        return self._run.get_status()

    def cancel(self):
        try:
            self._run.cancel()
            _logger.info("Job cancelled.")
        except KeyError as e:
            raise raise_from(RunEnvironmentException(), e)

    def _repr_html_(self):
        return self._run._repr_html_()
