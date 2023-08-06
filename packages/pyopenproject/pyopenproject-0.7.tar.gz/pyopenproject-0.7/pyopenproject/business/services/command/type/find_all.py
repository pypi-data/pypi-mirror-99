from pyopenproject.api_connection.exceptions.request_exception import RequestError
from pyopenproject.api_connection.requests.get_request import GetRequest
from pyopenproject.business.exception.business_error import BusinessError
from pyopenproject.business.services.command.find_list_command import FindListCommand
from pyopenproject.business.services.command.type.type_command import TypeCommand
from pyopenproject.model.type import Type


class FindAll(TypeCommand):

    def __init__(self, connection):
        super().__init__(connection)

    def execute(self):
        try:
            request = GetRequest(self.connection, f"{self.CONTEXT}")
            return FindListCommand(self.connection, request, Type).execute()
            # for typ in json_obj["_embedded"]["elements"]:
            #     yield Type(typ)
        except RequestError as re:
            raise BusinessError("Error finding all time entries") from re
