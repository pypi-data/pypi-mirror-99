import os
from cwrap import BaseCClass
from res import ResPrototype
from res.job_queue import WorkflowJob


class WorkflowJoblist(BaseCClass):
    TYPE_NAME = "workflow_joblist"
    _alloc = ResPrototype("void*            workflow_joblist_alloc()", bind=False)
    _free = ResPrototype("void             workflow_joblist_free(workflow_joblist)")
    _add_job = ResPrototype(
        "void             workflow_joblist_add_job(workflow_joblist, workflow_job)"
    )
    _add_job_from_file = ResPrototype(
        "bool             workflow_joblist_add_job_from_file(workflow_joblist, char*, char*)"
    )
    _has_job = ResPrototype(
        "bool             workflow_joblist_has_job(workflow_joblist, char*)"
    )
    _get_job = ResPrototype(
        "workflow_job_ref workflow_joblist_get_job(workflow_joblist, char*)"
    )
    _count = ResPrototype(
        "workflow_job_ref workflow_joblist_get_job(workflow_joblist, char*)"
    )

    def __init__(self):
        c_ptr = self._alloc()
        super(WorkflowJoblist, self).__init__(c_ptr)

    def addJob(self, job):
        """ @type job: WorkflowJob """
        job.convertToCReference(self)
        self._add_job(job)

    def addJobFromFile(self, name, filepath):
        """
        @type name: str
        @type filepath: str
        @rtype: bool
        """
        if not os.path.exists(filepath):
            raise UserWarning("Job file '%s' does not exist!" % filepath)

        return self._add_job_from_file(name, filepath)

    def __contains__(self, item):
        """
        @type item: str or WorkflowJob
        @rtype: bool
        """

        if isinstance(item, WorkflowJob):
            item = item.name()

        return self._has_job(item)

    def __getitem__(self, item):
        """
        @type item: str
        @rtype: WorkflowJob
        """

        if not item in self:
            return None

        return self._get_job(item)

    def free(self):
        self._free()
