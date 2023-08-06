#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Declare FastAPI events in this module (startup, shutdown, etc)
"""

from meerschaum.api import app, get_connector, get_uvicorn_config, debug
from meerschaum.utils.debug import dprint

@app.on_event("startup")
async def startup():
    from meerschaum.utils.misc import retry_connect
    import sys, os
    conn = get_connector()
    try:
        from meerschaum.utils.warnings import warn
        connected = await retry_connect(
            get_connector(),
            workers = get_uvicorn_config().get('workers', None),
            debug = debug
        )
    except Exception as e:
        print(e)
        connected = False
    if not connected:
        await shutdown()
        os._exit(1)

@app.on_event("shutdown")
async def shutdown():
    import os
    from meerschaum.config._paths import API_UVICORN_CONFIG_PATH
    try:
        if debug: dprint(f"Removing Uvicorn configuration ({API_UVICORN_CONFIG_PATH})")
        if API_UVICORN_CONFIG_PATH.exists():
            os.remove(API_UVICORN_CONFIG_PATH)
    except Exception as e:
        pass
        print(e)
    if debug: dprint("Closing connection...")
    if get_connector().type == 'sql':
        try:
            await get_connector().db.disconnect()
        except AssertionError:
            pass

