from checkov.graph.terraform.checks_infra.solvers.attribute_solvers.base_attribute_solver import BaseAttributeSolver


class ExistsAttributeSolver(BaseAttributeSolver):
    operator = 'exists'

    def __init__(self, resource_types, attribute, value):
        super().__init__(resource_types=resource_types,
                         attribute=attribute, value=value)

    def _get_operation(self, vertex, attribute):
        return vertex.get(attribute) is not None
