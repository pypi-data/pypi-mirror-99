from res.job_queue import Workflow
from res.util.substitution_list import SubstitutionList
from concurrent import futures


class WorkflowRunner(object):
    def __init__(self, workflow, ert=None, context=None):
        """
        @type workflow: Workflow
        @type ert: res.enkf.EnKFMain
        @type context: SubstitutionList
        """
        super(WorkflowRunner, self).__init__()

        self.__workflow = workflow
        self.__ert = ert

        if context is None:
            context = SubstitutionList()

        self.__context = context
        self.__workflow_result = None
        self._workflow_executor = futures.ThreadPoolExecutor(max_workers=1)
        self._workflow_job = None

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, type, value, traceback):
        self.wait()

    def run(self):
        if self.isRunning():
            raise AssertionError("An instance of workflow is already running!")
        else:
            self._workflow_job = self._workflow_executor.submit(self.__runWorkflow)

    def __runWorkflow(self):
        self.__workflow_result = self.__workflow.run(self.__ert, context=self.__context)

    def isRunning(self):
        """ @rtype: bool """
        if self.__workflow.isRunning():
            return True

        # Completion of _workflow does not indicate that __workflow_result is
        # set. Check future status, since __workflow_result follows future
        # completion.
        return self._workflow_job is not None and not self._workflow_job.done()

    def isCancelled(self):
        """ @rtype: bool """
        return self.__workflow.isCancelled()

    def cancel(self):
        if self.isRunning():
            self.__workflow.cancel()
        self.wait()

    def exception(self):
        if self._workflow_job is not None:
            return self._workflow_job._exception
        return None

    def wait(self):
        # This returns a tuple (done, pending), since we run only one job we don't need to use it
        _, _ = futures.wait(
            [self._workflow_job], timeout=None, return_when=futures.FIRST_EXCEPTION
        )

    def workflowResult(self):
        """ @rtype: bool or None """
        return self.__workflow_result

    def workflowReport(self):
        """ @rtype: {dict} """
        return self.__workflow.getJobsReport()

    def workflowError(self):
        """ @rtype: str """
        error = self.__workflow.getLastError()

        error_message = ""

        for error_line in error:
            error_message += error_line + "\n"

        return error_message
