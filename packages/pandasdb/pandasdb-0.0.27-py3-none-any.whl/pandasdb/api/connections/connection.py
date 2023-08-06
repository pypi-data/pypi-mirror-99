from functools import lru_cache

from pandasdb.sql.utils import string_to_python_attr, AutoComplete, generate_graph
from pandasdb.plot.graph import draw_graph
from pandasdb.connections.tunnel import Tunnel


class Connection:

    def __init__(self, name="", host="", schema="public", username="", password="", port=-1, database="", tunnel=None,
                 ssh_username=None, ssh_key=None, type=""):

        self.name = name
        self.db_type = type
        self.schema = schema
        self.tunnel = tunnel
        self.ssh_username = ssh_username
        self.ssh_key = ssh_key
        self.forwarder = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.reserved_words = []
        self._hidden_columns_included = False

    def graph(self, show=True, width=32, height=16):
        graph = None
        try:
            graph = self._graph()
        except:
            graph = self._graph_from_column_names()
        finally:
            if show:
                draw_graph(graph, (width, height))
            else:
                return graph

    @lru_cache
    def neighbours(self, table):
        G = self.graph(show=False)

        nbrs = []
        for name in G.neighbors(table.name):
            nbrs.append(getattr(self.Tables, name))

        return nbrs

    @property
    def conn(self):
        return Tunnel(self._conn_func, host=self.host, username=self.username, password=self.password, port=self.port,
                      database=self.database, tunnel=self.tunnel, ssh_username=self.ssh_username,
                      ssh_key=self.ssh_key)

    @property
    def engine(self):
        return Tunnel(self._engine_func, host=self.host, username=self.username, password=self.password, port=self.port,
                      database=self.database, tunnel=self.tunnel, ssh_username=self.ssh_username,
                      ssh_key=self.ssh_key)

    def toggle_hidden_columns(self, included=True):
        self._hidden_columns_included = included
        self._extract_tables()

    @property
    def Tables(self):
        try:
            return self._TAB
        except AttributeError:
            self._extract_tables()
            return self._TAB

    def _extract_tables(self):
        TAB = AutoComplete("Tables", {string_to_python_attr(table.name): table for table in self.get_tables()})
        setattr(self, "_TAB", TAB)

    def _engine_func(self):
        raise NotImplementedError("engine() should be implemented by all children")

    def _conn_func(self):
        raise NotImplementedError("_conn_func() should be implemented by all children")

    def stream(self, sql, batch_size):
        raise NotImplementedError("stream() should be implemented by all children")

    # def accepted_types(self, operator):
    #     raise NotImplementedError("accepted_types(operator) should be implemented by all children")

    def query(self, action, columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "query( action, columns, table_name, joins, where, groups, having, meta) should be implemented by all children")

    def execute(self, action, target_columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "execute( action, target_columns, table_name, joins, where, groups, having, meta) should be implemented by all children")

    def optimize(self, action, target_columns, table_name, joins, where, groups, having, meta):
        raise NotImplementedError(
            "optimize( action, target_columns, table_name, joins, where_conditions, groups, having_conditions, meta) should be implemented by all children")

    def get_tables(self, with_columns):
        raise NotImplementedError("get_tables() should be implemented by all children")

    def get_columns(self, table):
        raise NotImplementedError("get_columns(table) should be implemented by all children")

    @lru_cache
    def _graph_from_column_names(self):
        return generate_graph(self.Tables)

    @lru_cache
    def _graph(self):
        raise NotImplementedError("_graph() should be implemented by all children")
