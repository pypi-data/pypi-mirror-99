"""Archey configuration module"""

from copy import deepcopy

import json
import logging
import os

from archey.singleton import Singleton
from archey.utility import Utility


# Below are default required configuration keys which will be used.
DEFAULT_CONFIG = {
    'allow_overriding': True,
    'parallel_loading': True,
    'suppress_warnings': False,
    'honor_ansi_color': True,
    'default_strings': {
        'latest': 'latest',
        'available': 'available',
        'no_address': 'No Address',
        'not_detected': 'Not detected',
        'virtual_environment': 'Virtual Environment'
    }
}


class Configuration(metaclass=Singleton):
    """
    Values present in `DEFAULT_CONFIG` dictionary are required.
    New optional values may be added with `Utility.update_recursive` method.

    If a `config_path` is passed during instantiation, it will be loaded.
    """
    def __init__(self, config_path=None):
        # Deep-copy `DEFAULT_CONFIG` so we have a local copy to safely mutate.
        self._config = deepcopy(DEFAULT_CONFIG)

        # If a `config_path` has been specified, (try to) load it directly.
        if config_path:
            self._load_configuration(config_path)
        # If not, load each (optional) configuration file in a "regular" order.
        else:
            self._load_configuration('/etc/archey4/')
            self._load_configuration(os.path.expanduser('~/.config/archey4/'))
            self._load_configuration(os.getcwd())

    def get(self, key: str, default=None):
        """
        A binding method to imitate the `dict.get()` behavior.
        """
        return self._config.get(key, default)

    def _load_configuration(self, path: str):
        """
        A method handling configuration loading from a JSON file.
        It will try to load any `config.json` present under `path`.
        """
        # If a previous configuration file has denied overriding...
        if not self.get('allow_overriding'):
            #  ... don't load this one.
            return

        # If the specified `path` is a directory, append the file name we are looking for.
        if os.path.isdir(path):
            path = os.path.join(path, 'config.json')

        try:
            with open(path) as f_config:
                Utility.update_recursive(self._config, json.load(f_config))
        except FileNotFoundError:
            return
        except json.JSONDecodeError as json_decode_error:
            logging.error('%s (%s)', json_decode_error, path)
            return

        # When `suppress_warnings` is set, higher the log level to silence warning messages.
        logging.getLogger().setLevel(
            logging.ERROR if self.get('suppress_warnings') else logging.WARN
        )

    def __iter__(self):
        """When used as an iterator, directly yield `_config` elements"""
        return iter(self._config.items())
