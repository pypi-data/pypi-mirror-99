#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
This module contains SQLConnector functions for executing SQL queries.
"""

from __future__ import annotations
from meerschaum.utils.typing import (
    Union, Mapping, List, Dict, SuccessTuple, Optional, Any, Sequence, Iterable, Callable
)

from meerschaum.utils.debug import dprint
from meerschaum.utils.warnings import warn

### database flavors that can use bulk insert
bulk_flavors = {'postgresql', 'timescaledb'}

def read(
        self,
        query_or_table : Union[str, sqlalchemy.Query],
        params : Optional[Dict[str, Any], List[str]] = {},
        chunksize : Optional[int] = -1,
        chunk_hook : Optional[Callable[[pandas.DataFrame], Any]] = None,
        as_hook_results : bool = False,
        chunks : Optional[int] = None,
        as_chunks : bool = False,
        as_iterator: bool = False,
        silent : bool = False,
        debug : bool = False,
        **kw : Any
    ) -> Optional[
            Union[
                pandas.DataFrame,
                List[pandas.DataFrame],
                List[Any],
            ]
        ]:
    """
    Read a SQL query or table into a pandas dataframe.

    :param query_or_table:
        The SQL query (sqlalchemy Query or string) or name of the table from which to select.

    :param params:
        `List` or `Dict` of parameters to pass to `pandas.read_sql()`.
        See the pandas documentaion for more information:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html

    :param chunksize:
        How many chunks to read at a time. `None` will read everything in one large chunk.
        Defaults to system configuration.

    :param chunk_hook:
        Hook function to execute once per chunk.
        NOTE: `as_iterator` MUST be False (default).
        E.g. Write and reading chunks intermittently. See `--sync-chunks` for an example.

    :param as_hook_results:
        If `True`, return a `List` of the outputs of the hook function.
        Only applicable if `chunk_hook` is not None.
        NOTE: `as_iterator` MUST be False (default).
        Defaults to False.

    :param chunks:
        How many chunks to retrieve and return into a single dataframe.

    :param as_chunks:
        If `True`, return a list of DataFrames. Otherwise return a single DataFrame.
        Defaults to False.

    :param as_iterator:
        If `True`, return the pandas DataFrame iterator.
        `chunksize` must not be None (falls back to 1000 if so),
            and hooks are not called in this case.
        Defaults to False.

    :param silent:
        If `True`, don't raise warnings in case of errors.
        Defaults to `False`.

    """
    if chunks is not None and chunks <= 0: return []
    from meerschaum.utils.misc import sql_item_name
    from meerschaum.utils.packages import attempt_import, import_pandas
    pd = import_pandas()
    sqlalchemy = attempt_import("sqlalchemy")
    chunksize = chunksize if chunksize != -1 else self.sys_config.get('chunksize', None)
    if chunksize is None and as_iterator:
        if not silent:
            warn(f"An iterator may only be generated if chunksize is not None. Falling back to a chunksize of 1000.", stacklevel=3)
        chunksize = 1000
    if debug:
        import time
        start = time.time()
        dprint(query_or_table)
        dprint(f"Fetching with chunksize: {chunksize}")

    ### This might be sqlalchemy object or the string of a table name.
    ### We check for spaces and quotes to see if it might be a weird table.
    if (
        ' ' not in str(query_or_table)
        or (
            ' ' in str(query_or_table)
            and str(query_or_table).startswith('"')
            and str(query_or_table).endswith('"')
        )
    ):
        query_or_table = sql_item_name(str(query_or_table), self.flavor)
        if debug: dprint(f"Reading from table {query_or_table}")
        formatted_query = str(sqlalchemy.text("SELECT * FROM " + str(query_or_table)))
    else:
        try:
            formatted_query = str(sqlalchemy.text(query_or_table))
        except:
            formatted_query = query_or_table

    try:
        chunk_generator = pd.read_sql(
            formatted_query,
            self.engine,
            params = params,
            chunksize = chunksize
        )
    except Exception as e:
        import inspect
        if debug: dprint(f"Failed to execute query:\n\n{query_or_table}\n\n")
        if not silent: warn(str(e))

        return None

    chunk_list = []
    read_chunks = 0
    chunk_hook_results = []
    if chunksize is None:
        chunk_list.append(chunk_generator)
    elif as_iterator:
        return chunk_generator
    else:
        for chunk in chunk_generator:
            if chunk_hook is not None:
                chunk_hook_results.append(
                    chunk_hook(chunk, chunksize=chunksize, debug=debug, **kw)
                )
            chunk_list.append(chunk)
            read_chunks += 1
            if chunks is not None and read_chunks >= chunks:
                break

    ### If no chunks returned, read without chunks
    ### to get columns
    if len(chunk_list) == 0:
        chunk_list.append(
            pd.read_sql(
                formatted_query,
                self.engine
            )
        )

    ### call the hook on any missed chunks.
    if chunk_hook is not None and len(chunk_list) > len(chunk_hook_results):
        for c in chunk_list[len(chunk_hook_results):]:
            chunk_hook_results.append(
                chunk_hook(chunk, chunksize=chunksize, debug=debug, **kw)
            )

    ### chunksize is not None so must iterate
    if debug:
        end = time.time()
        dprint(f"Fetched {len(chunk_list)} chunks in {round(end - start, 2)} seconds.")

    if as_hook_results:
        return chunk_hook_results
    
    ### Skip `pd.concat()` if `as_chunks` is specified.
    if as_chunks:
        for c in chunk_list:
            c.reset_index(drop=True, inplace=True)
        return chunk_list

    return pd.concat(chunk_list).reset_index(drop=True)

def value(
        self,
        query : str,
        *args : Any,
        **kw : Any
    ) -> Any:
    """
    Return a single value from a SQL query
    (index a DataFrame at [0, 0])
    """
    try:
        return self.read(query, *args, **kw).iloc[0, 0]
    except:
        return None

def execute(
        self,
        *args : Any,
        **kw : Any
    ) -> Optional[sqlalchemy.engine.result.resultProxy]:
    return self.exec(*args, **kw)

def exec(
        self,
        query : str,
        *args : Any,
        silent : bool = False,
        debug : bool = False,
        **kw : Any
    ) -> Optional[sqlalchemy.engine.result.resultProxy]:
    """
    Execute SQL code and return success status. e.g. calling stored procedures.

    Wrapper for self.engine.connect() and connection.execute().

    If inserting data, please use bind variables to avoid SQL injection!
    """
    from meerschaum.utils.debug import dprint
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import("sqlalchemy")
    if debug: dprint("Executing query:\n" + f"{query}")
    try:
        with self.engine.connect() as connection:
            result = connection.execute(
                query,
                *args,
                **kw
            )
    except Exception as e:
        import inspect

        if debug: dprint(f"Failed to execute query:\n\n{query}\n\n")
        if not silent: warn(str(e))
        result = None

    return result

def to_sql(
        self,
        df : pandas.DataFrame,
        name : str = None,
        index : bool = False,
        if_exists : str = 'replace',
        method : str = "",
        chunksize : int = -1,
        silent : bool = False,
        debug : bool = False,
        as_tuple : bool = False,
        **kw
    ) -> Union[bool, SuccessTuple]:
    """
    Upload a DataFrame's contents to the SQL server

    :param df:
        The DataFrame to be uploaded

    :param name:
        The name of the table to be created

    :param index:
        If True, creates the DataFrame's indices as columns (default False)

    :param if_exists: str
        ['replace', 'append', 'fail']
        Drop and create the table ('replace') or append if it exists ('append') or raise Exception ('fail')
        (default 'replace')

    :param method:
        None or multi. Details on pandas.to_sql

    :param as_tuple:
        If True, return a (success_bool, message) tuple instead of a bool

    **kw : keyword arguments
        Additional arguments will be passed to the DataFrame's `to_sql` function
    """
    import time
    from meerschaum.utils.warnings import error
    if name is None:
        error("Name must not be None to submit to the SQL server")

    from meerschaum.utils.misc import sql_item_name

    ### resort to defaults if None
    if method == "":
        if self.flavor in bulk_flavors:
            method = psql_insert_copy
        else:
            method = self.sys_config['method']
    chunksize = chunksize if chunksize != -1 else self.sys_config['chunksize']

    success, msg = False, "Default to_sql message"
    start = time.time()
    if debug:
        msg = f"Inserting {len(df)} rows with chunksize: {chunksize}..."
        print(msg, end="", flush=True)

    ### filter out non-pandas args
    import inspect
    to_sql_params = inspect.signature(df.to_sql).parameters
    to_sql_kw = dict()
    for k, v in kw.items():
        if k in to_sql_params:
            to_sql_kw[k] = v

    try:
        df.to_sql(
            name = name,
            con = self.engine,
            index = index,
            if_exists = if_exists,
            method = method,
            chunksize = chunksize,
            **to_sql_kw
        )
        success = True
    except Exception as e:
        if not silent: warn(str(e))
        success, msg = None, str(e)

    end = time.time()
    if success:
        msg = f"It took {round(end - start, 2)} seconds to sync {len(df)} rows to {name}."

    if debug:
        print(f" done.", flush=True)
        dprint(msg)

    if as_tuple: return success, msg
    return success

def psql_insert_copy(
        table : pandas.io.sql.SQLTable,
        conn : Union[sqlalchemy.engine.Engine, sqlalchemy.engine.Connection],
        keys : Sequence[str],
        data_iter : Iterable[Any]
    ) -> None:
    """
    Execute SQL statement inserting data

    :param table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    import csv
    from io import StringIO

    from meerschaum.utils.misc import sql_item_name

    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(sql_item_name(table.schema, 'postgresql'), sql_item_name(table.name, 'postgresql'))
        else:
            table_name = sql_item_name(table.name, 'postgresql')

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns
        )
        cur.copy_expert(sql=sql, file=s_buf)
