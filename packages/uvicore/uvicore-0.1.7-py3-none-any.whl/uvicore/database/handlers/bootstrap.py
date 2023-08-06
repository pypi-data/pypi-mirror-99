import uvicore
from uvicore.typing import Dict
from uvicore.events import Handler
from uvicore.support.module import load
from uvicore.support.dumper import dump, dd
from uvicore.foundation.events.app import Booted as OnAppBooted


class Database(Handler):

    def __call__(self, event: OnAppBooted):
        """Bootstrap the Database after the Application is Booted"""

        #from uvicore.console.console import cli        # Gather all connections, models, tables
        # No need to gather seeder classes, I get those in the ./uvicore db seed command
        connections = Dict()
        models = []; tables = []
        last_default = None; app_default = None
        for package in uvicore.app.packages.values():
            if not 'database' in package: continue

            # Get last defined default connection
            if package.database.connection_default: last_default = package.database.connection_default

            # Get running app default connection
            if package.main and package.database.connection_default: app_default = package.database.connection_default

            # Append connections
            #connections.extend(package.database.connections or [])
            connections.merge(package.database.connections)
            #connections.merge(package.database)

            # Append models
            models.extend(package.database.models or [])

            # Append tables
            tables.extend(package.database.tables or [])

        # Initialize Database with all connections at once
        uvicore.db.init(app_default or last_default, connections)

        # Dynamically Import models, tables and seeders
        for model in models: load(model)
        for table in tables: load(table)
