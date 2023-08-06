#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Functions for managing plugins registration via the SQL connector
"""

from __future__ import annotations
from meerschaum.utils.typing import Optional, Any, List, SuccessTuple, Dict

def register_plugin(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False,
        **kw : Any
    ) -> SuccessTuple:
    """
    Register a new plugin
    """

    from meerschaum.utils.warnings import warn, error
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']

    old_id = self.get_plugin_id(plugin, debug=debug)

    if old_id is not None:
        old_version = self.get_plugin_version(plugin, debug=debug)
        new_version = plugin.version
        if old_version is None: old_version = ''
        if new_version is None: new_version = ''

        ### verify that the new version is greater than the old
        from packaging import version as packaging_version
        if packaging_version.parse(old_version) >= packaging_version.parse(new_version):
            return False, (
                f"Version '{new_version}' of plugin '{plugin}' must be greater than existing version '{old_version}'."
            )

    import json
    bind_variables = {
        'plugin_name' : plugin.name,
        'version' : plugin.version,
        'attributes' : json.dumps(plugin.attributes),
        'user_id' : plugin.user_id,
        #  'plugin_id' : old_id,
    }

    if old_id is None:
        query = sqlalchemy.insert(plugins).values(**bind_variables)
    else:
        query = (
            sqlalchemy.update(plugins).
            values(**bind_variables).
            where(plugins.c.plugin_id == old_id)
        )

    result = self.exec(query, debug=debug)
    if result is None:
        return False, f"Failed to register plugin '{plugin}'"
    return True, f"Successfully registered plugin '{plugin}'"

def get_plugin_id(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False
    ) -> Optional[int]:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = sqlalchemy.select([plugins.c.plugin_id]).where(plugins.c.plugin_name == plugin.name)
    
    try:
        return int(self.value(query, debug=debug))
    except:
        return None

def get_plugin_version(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False
    ) -> str:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = sqlalchemy.select([plugins.c.version]).where(plugins.c.plugin_name == plugin.name)

    return self.value(query, debug=debug)

def get_plugin_user_id(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False
    ) -> Optional[int]:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = sqlalchemy.select([plugins.c.user_id]).where(plugins.c.plugin_name == plugin.name)

    try:
        return int(self.value(query, debug=debug))
    except:
        return None

def get_plugin_username(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False
    ) -> str:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    users = get_tables(mrsm_instance=self, debug=debug)['users']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = (
        sqlalchemy.select([users.c.username]).
        where(
            users.c.users_id == plugins.c.user_id
            and plugins.c.plugin_name == plugin.name
        )
    )

    #  query = f"""
    #  SELECT users.username
    #  FROM plugins
    #  INNER JOIN users ON users.user_id = plugins.user_id
    #  WHERE plugin_name = %(plugin_name)s
    #  """
    return self.value(query, debug=debug)

def get_plugin_attributes(
        self,
        plugin : 'meerschaum._internal.Plugin.Plugin',
        debug : bool = False
    ) -> Dict[str, Any]:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = sqlalchemy.select([plugins.c.attributes]).where(plugins.c.plugin_name == plugin.name)

    return self.value(query, debug=debug)

def get_plugins(
        self,
        user_id : Optional[int] = None,
        search_term : Optional[str] = None,
        debug : bool = False,
        **kw : Any
    ) -> List[str]:
    ### ensure plugins table exists
    from meerschaum.connectors.sql.tables import get_tables
    plugins = get_tables(mrsm_instance=self, debug=debug)['plugins']
    from meerschaum.utils.packages import attempt_import
    sqlalchemy = attempt_import('sqlalchemy')

    query = sqlalchemy.select([plugins.c.plugin_name])
    if user_id is not None:
        query = query.where(plugins.c.user_id == user_id)
    if search_term is not None:
        query = query.where(plugins.c.plugin_name.like(search_term + '%'))

    #  q = f"""
    #  SELECT plugin_name
    #  FROM plugins
    #  """ + ("""
    #  WHERE user_id = %(user_id)s
    #  """ if user_id is not None else "")

    return list(self.read(query, debug=debug)['plugin_name'])

