import uvicore
from uvicore.typing import Any, Dict
from uvicore.package import ServiceProvider
from uvicore.support.dumper import dump, dd
from uvicore.support.module import load
from uvicore.console.provider import Cli
from uvicore.database.handlers import bootstrap
from uvicore.foundation.events import app as AppEvents
from uvicore.http.events import server as HttpEvents


@uvicore.provider()
class Database(ServiceProvider, Cli):

    def register(self) -> None:
        # Register IoC bindings
        # self.bind('Database', 'uvicore.database.db._Db',
        #     singleton=True,
        #     aliases=['database', 'db'],
        # )

        # Set uvicore.log global
        uvicore.db = uvicore.ioc.make('uvicore.database.db.Db')

        # Register event listeners
        AppEvents.Booted.listen(bootstrap.Database)
        HttpEvents.Startup.listen(uvicore.db.http_startup)

    def boot(self) -> None:

        # Define service provider registration control
        self.registers(self.package.config.registers)

        # Define db commands
        self.commands(
            group='db',
            help='Database Commands',
            commands={
                'create': 'uvicore.database.commands.db.create',
                'drop': 'uvicore.database.commands.db.drop',
                'recreate': 'uvicore.database.commands.db.recreate',
                'seed': 'uvicore.database.commands.db.seed',
                'reseed': 'uvicore.database.commands.db.reseed',
                'connections': 'uvicore.database.commands.db.connections',
            }
        )

        # Extend schematic generator commands
        self.commands(
            group='gen',
            commands={
                'table': 'uvicore.database.commands.generators.table',
                'seeder': 'uvicore.database.commands.generators.seeder',
            }
        )
