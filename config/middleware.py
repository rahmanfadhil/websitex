from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META["PATH_INFO"] == "/ping/":
            executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            status = 503 if plan else 200
            return HttpResponse(status=status)
