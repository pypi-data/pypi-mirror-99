from checkov.graph.terraform.checks_infra.solvers.connections_solvers.connection_exists_solver import ConnectionExistsSolver


class ConnectionNotExistsSolver(ConnectionExistsSolver):
    operator = 'not_exists'

    def __init__(self, resource_types, connected_resources_types, vertices_under_resource_types=None, vertices_under_connected_resources_types=None):
        super().__init__(resource_types, connected_resources_types, vertices_under_resource_types, vertices_under_connected_resources_types)

    def run(self, graph_connector):
        passed, failed = super().run(graph_connector)
        return failed, passed

