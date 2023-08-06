"""Extensible table data structure.

Table data structure that supports the introduction of user-defined workflow
combinators and the use of these combinators in concise workflow descriptions.
"""

from __future__ import annotations
import doctest
import itertools
import symbolism

class row: # pylint: disable=R0903
    """
    Symbolic representation of a row index.
    """

class column(symbolism.symbol): # pylint: disable=R0903
    """
    Symbolic representation of a column specified (i.e.,
    a numerical index or an attribute name).
    """

class metatable:
    """
    Class for the extensible metatable data structure.
    """
    @staticmethod
    def _eval(r, i, e):
        """
        Evaluation of a symbolic expression that may contain
        references to specific attributes/columns of a row.
        """
        if isinstance(e, column):
            return r[e.evaluate()]

        if e is row:
            return i

        if isinstance(e, symbolism.symbol):
            return\
                e.evaluate()\
                if len(e) == 0 else\
                e.instance(*[metatable._eval(r, i, p) for p in e.parameters])

        return e

    @staticmethod
    def _upd(update_filter_index_row):
        """
        Internal method for the work to be completed for each row
        during an invocation of an update on the table.
        """
        ((update, filter_), (index, row_)) = update_filter_index_row

        for col in update:
            while col > len(row_) - 1:
                row_.append(None)

        for (col_, upd) in update.items():
            row_[col_] = metatable._eval(row_, index, upd)

        return [row_] if filter_ is None or metatable._eval(row_, index, filter_) else []

    def __init__(self, iterable, name=None, header=False):
        """
        Constructor for a table instance that draws data from an iterable.
        """
        self.iterable = iterable
        self.name = name
        self.header = header

    def __iter__(self):
        """
        An instance of a table is an iterable.
        """
        for row_ in self.iterable:
            yield row_

    def map(self, function, iterable, progress): # pylint: disable=R0201
        """
        Internal method for mapping over the data in the table. This method
        can be redefined in derived classes to change how rows are processed
        (e.g., to introduce multiprocessing).
        """
        return (row for rows in progress(map(function, iterable)) for row in rows)

    def update_filter(self, update, filter, progress=lambda _: _): # pylint: disable=W0622
        """
        Update-then-filter operations across the entire table, based on
        symbolic expressions for the update and filter task(s).

        >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
        >>> t.update_filter({0: column(1)}, column(1) > symbolism.symbol(0))
        [[1, 1], [2, 2]]
        >>> list(t)
        [[1, 1], [2, 2]]
        >>> t = metatable([['a'], ['b'], ['c']])
        >>> t.update_filter({3: row}, column(3) < 2)
        [['a', None, None, 0], ['b', None, None, 1]]
        >>> list(t)
        [['a', None, None, 0], ['b', None, None, 1]]
        """
        (rows_in, rows_out) = (iter(self), [])

        if self.header:
            for row_ in rows_in:
                rows_out.append(row_)
                break

        rows_out.extend(self.map(
            metatable._upd,
            zip(itertools.repeat((update, filter)), enumerate(rows_in)),
            progress
        ))

        self.iterable = rows_out
        return rows_out

    def update(self, update, progress=lambda _: _):
        """
        Update operation across the entire table, based on a
        symbolic expression for the update task(s).

        >>> t = metatable([['a', 0], ['b', 1], ['c', 2]])
        >>> t.update({0: column(1)}) # Replace first-column value with second-column value.
        [[0, 0], [1, 1], [2, 2]]
        >>> list(t)
        [[0, 0], [1, 1], [2, 2]]
        >>> t = metatable([['char', 'num'], ['a', 0], ['b', 1]], header=True)
        >>> t.update({1: column(0)})
        [['char', 'num'], ['a', 'a'], ['b', 'b']]
        """
        return self.update_filter(update, None, progress)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
