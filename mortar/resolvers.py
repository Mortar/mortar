from mush import Requirement, missing, Value, requires as mortar_requires
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


def combine_requires(*all_requires):
    final = []
    for requires in all_requires:
        if requires is not None:
            if isinstance(requires, (tuple, list)):
                final.extend(requires)
            else:
                final.append(requires)
    return mortar_requires(*(
        requirement_modifier(Requirement(r, name=r) if not isinstance(r, Requirement) else r)
        for r in final
    ))
