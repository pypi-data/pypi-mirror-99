import configparser
import importlib.machinery
import importlib.util
import os
import site
import sys

from metadatadb_driver_interface.constants import CONFIG_OPTION
from metadatadb_driver_interface.exceptions import ConfigError


def parse_config(file_path):
    """Loads the configuration file given as parameter"""
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    plugin_config = {}
    options = config_parser.options(CONFIG_OPTION)
    for option in options:
        try:
            plugin_config[option] = config_parser.get(CONFIG_OPTION, option)
            if plugin_config[option] == -1:
                print("skip: %s" % option)
        except Exception as e:
            print("exception on %s!" % option)
            print(e.message)
            plugin_config[option] = None
    return plugin_config


def start_plugin(file_path=None):
    """This function initialize the MetadataDB plugin"""
    if os.getenv('CONFIG_PATH'):
        file_path = os.getenv('CONFIG_PATH')
    else:
        file_path = file_path
    if file_path is not None:
        config = parse_config(file_path)
        plugin_instance = load_plugin(config)
    else:
        plugin_instance = load_plugin
    return plugin_instance


def load_plugin(config=None):
    try:
        module = get_value('module', 'MODULE', 'elasticsearch', config)
        if 'module.path' in config:
            module_path = config['module.path']
        elif os.getenv('VIRTUAL_ENV') is not None:
            module_path = "%s/lib/python3.%s/site-packages/metadata_driver_%s/plugin.py" % (
                os.getenv('VIRTUAL_ENV'), sys.version_info[1], module)
        else:
            module_path = "%s/metadata_driver_%s/plugin.py" % (
                site.getsitepackages()[0], module)
    except Exception:
        raise ConfigError("You should provide a valid config.")
    if sys.version_info < (3, 5):
        from importlib.machinery import SourceFileLoader

        mod = SourceFileLoader("plugin.py", module_path).load_module()
        return mod.Plugin(config)
    else:
        spec = importlib.util.spec_from_file_location("plugin.py", module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.Plugin(config)


def get_value(value, env_var, default, config=None):
    if os.getenv(env_var) is not None:
        return os.getenv(env_var)
    elif config is not None and value in config:
        return config[value]
    else:
        return default
