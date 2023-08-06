#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Generic Connector parent class. Reads attributes from the configuration.
Consult implemented child classes like SQLConnector, APIConnector, MQTTConnector, or
PluginConnector for further details.
"""

from __future__ import annotations
import abc
from meerschaum.utils.typing import Iterable, Optional, Any, Union

class Connector(metaclass=abc.ABCMeta):
    def __init__(
            self,
            type : Optional[str] = None,
            label : Optional[str] = None,
            **kw : Any
        ):
        """
        type : str
            The type of the connection. Used as a key in config.yaml to get attributes.
            Supported values are 'sql', 'api', 'mqtt', 'plugin'.

        label : str
            The label for the connection. Used as a key within config.yaml

        pandas : str
            Custom pandas implementation name.
            May change to modin.pandas soon.

        If config.yaml is set for the given type and label, the hierarchy looks like so:
        meerschaum:
            connections:
                {type}:
                    {label}:
                        ### attributes go here

        Read config.yaml for attributes partitioned by connection type and connection label.
        Example: type="sql", label="main"
        """
        self._original_dict = self.__dict__.copy()
        self._set_attributes(type=type, label=label, **kw)

    def _reset_attributes(self):
        self.__dict__ = self._original_dict

    def _set_attributes(
            self,
            type : Optional[str] = None,
            label : str = "main",
            pandas : Optional[str] = None,
            inherit_default : bool = True,
            **kw : Any
        ):
        from meerschaum.utils.warnings import error
        if label == 'default':
            error("Label cannot be 'default'. Did you mean 'main'?")
        self.type, self.label = type, label

        from meerschaum.config import get_config
        conn_configs = get_config('meerschaum', 'connectors')
        connector_config = get_config('system', 'connectors')

        ### inherit attributes from 'default' if exists
        if inherit_default:
            inherit_from = 'default'
            if self.type in conn_configs and inherit_from in conn_configs[self.type]:
                self.__dict__.update(conn_configs[self.type][inherit_from])

        ### load user config into self.__dict__
        if self.type in conn_configs and self.label in conn_configs[self.type]:
            self.__dict__.update(conn_configs[self.type][self.label])

        ### load system config into self.sys_config
        ### (deep copy so future Connectors don't inherit changes)
        if self.type in connector_config:
            from copy import deepcopy
            self.sys_config = deepcopy(connector_config[self.type])

        ### add additional arguments or override configuration
        self.__dict__.update(kw)

    def verify_attributes(
            self,
            required_attributes : set = {
                'label'
            },
            debug : bool = False
        ):
        """
        Ensure that the required attributes have been met.
        
        required_attributes : set
            Attributes to be verified.

        The Connector base class checks the minimum requirements.
        Child classes may enforce additional requirements.
        """
        from meerschaum.utils.warnings import error, warn
        from meerschaum.utils.debug import dprint
        if debug:
            dprint(f'required attributes: {required_attributes}')
            dprint(f'attributes: {self.__dict__}')
        missing_attributes = set()
        for a in required_attributes:
            if a not in self.__dict__:
                missing_attributes.add(a)
        if len(missing_attributes) > 0:
            error(
                f"Please provide connection configuration for connector '{self.type}:{self.label}' "
                f"in the configuration file (open with `mrsm edit config`) or as arguments for the Connector.\n\n"
                f"Missing attributes: {missing_attributes}",
                silent = True,
                stack = False
            )

    def fetch(
            self,
            instructions : dict
        ) -> 'pd.DataFrame':
        """
        Abstract method for all Connectors.
        In addition to specialized functionality, all Connectors must be able to fetch data
        based on criteria provided in the instructions dictionary.

        Returns pandas (or pandas derivative) DataFrame
        """
        from meerschaum.utils.warnings import error
        error("fetch() must be implemented in children classes", NotImplementedError)

    def __str__(self):
        return f"{self.type}:{self.label}"

    def __repr__(self):
        return str(self)
