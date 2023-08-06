from pyopenproject.api_connection.exceptions.request_exception import RequestError
from pyopenproject.api_connection.requests.get_request import GetRequest
from pyopenproject.business.exception.business_error import BusinessError
from pyopenproject.business.services.command.find_list_command import FindListCommand
from pyopenproject.business.services.command.work_package.work_package_command import WorkPackageCommand
from pyopenproject.model.project import Project


class FindAvailableProjects(WorkPackageCommand):
    def __init__(self, connection, work_package=None):
        super().__init__(connection)
        self.context = f"{work_package.id}/available_projects" if work_package else "available_projects"
        self.work_package = work_package

    def execute(self):
        try:
            request = GetRequest(self.connection,
                                  f"{self.CONTEXT}/{self.context}")
            return FindListCommand(self.connection, request, Project).execute()
            # for project in json_obj["_embedded"]["elements"]:
            #     yield p.Project(project)
        except RequestError as re:
            raise BusinessError(f"Error finding available projects for work package {self.work_package.id}") from re
