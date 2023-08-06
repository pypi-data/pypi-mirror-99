import sqlparse
from ibis.expr.api import ColumnExpr
import pandas as pd


class Column:
    def __init__(self, ibis_column: ColumnExpr, table):
        self._column = ibis_column
        self._table = table

        self.full_name = f"{repr(self._table)}.{self._column.get_name()}"
        self.name = self._column.get_name()
        self.dtype = self._column.type()

        # Add all the functions of the ibis function to the column
        # self._fetch_and_wrap_inner_column_funcs()

    @property
    def sql(self):
        return sqlparse.format(str(self._column.compile()), reindent=True, keyword_case='upper')

    def _fetch_and_wrap_inner_column_funcs(self):
        def wrapper(func_name):
            return Column(getattr(self._column, func_name), self._table)

        column_functions = []
        for attr in self._column.__dir__():
            if not attr.startswith("_") and not attr.endswith("_") and callable(getattr(self._column, attr)):
                column_functions.append(attr)

        for func_name in column_functions:
            if not hasattr(self, func_name):
                setattr(self, func_name, lambda: wrapper(func_name=func_name))

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return getattr(self._column, item)

    def alias(self, name):

        return self._column.name(name)

    def head(self, n=5):
        return self._table[[self]].head(n)

    def isin(self, arr):
        return self._column.isin(arr)

    def notint(self, arr):
        return self._column.notin(arr)

    def df(self):
        return self._table[[self]].df()

    def __add__(self, other):
        return self._column.add(other)

    def __radd__(self, other):
        return self._column.add(other)

    def __sub__(self, other):
        return self._column.sub(other)

    def __rsub__(self, other):
        return self._column.add(-other)

    def __truediv__(self, other):
        return self._column / other

    def __rtruediv__(self, other):
        return other._column / self

    def __and__(self, other):
        return self._column and other

    def __rand__(self, other):
        return other and self._column

    def __or__(self, other):
        return self._column or other

    def __ror__(self, other):
        return other or self._column

    def __invert__(self):
        return not self._column

    def __lt__(self, other):
        return self._column < other

    def __rlt__(self, other):
        return other < self._column

    def __le__(self, other):
        return self._column <= other

    def __rle__(self, other):
        return other <= self._column

    def __eq__(self, other):
        if isinstance(other, Column):
            return self._column == other._column
        elif pd.isna(other):
            return self._column.isnull()
        else:
            return self._column == other

    def __req__(self, other):
        return other == self._column if not isinstance(other, Column) and not pd.isna(other) else self._column.isnull()

    def __ne__(self, other):
        return self._column != other if not isinstance(other, Column) and not pd.isna(other) else self._column.notnull()

    def __rne__(self, other):
        return self._column != other if not isinstance(other, Column) and not pd.isna(other) else self._column.notnull()

    def __ge__(self, other):
        return self._column >= other

    def __rge__(self, other):
        return other >= self._column

    def __gt__(self, other):
        return self._column > other

    def __rgt__(self, other):
        return other < self._column

    def __hash__(self):
        return hash(self.full_name)

    def __str__(self):
        return self.full_name

    def _repr_html_(self):
        return self.head().to_html()
