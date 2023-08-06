import ibis

from pandasdb.io.connection.connection import Connection


class PostgreSQLConnection(Connection):

    def __init__(self, name="", host="", schema="public", username="", password="", port=-1, database="", tunnel=None,
                 ssh_username=None, ssh_key=None, type=""):
        Connection.__init__(self, ibis.postgres.connect, name=name, host=host, schema=schema, username=username,
                            password=password,
                            port=port, database=database, tunnel=tunnel, ssh_username=ssh_username, ssh_key=ssh_key,
                            type=type)
