from mush import Requirement, missing, Value
from starlette.requests import Request


class FromRequest(Requirement):

    def resolve(self, context):
        request = context.get(Request)
        value = request.path_params.get(self.name, missing)
        if value is missing:
            value = request.query_params.get(self.name, missing)
        if value is missing:
            return self.default
        if self.type is not None:
            return self.type(value)
        return value


def requirement_modifier(requirement):
    if type(requirement) is Requirement:
        if requirement.type in (str, int, float, None):
            type_ = FromRequest
        else:
            type_ = Value
        requirement = type_.make_from(requirement)
    return requirement
