import ibis

from pandasdb.io.config.configuration import Configuration
from pandasdb.io.connection.connection import Connection


class PostgreSQLConnection(Connection):

    def __init__(self, configuration: Configuration):
        Connection.__init__(self, ibis.postgres.connect, configuration)
