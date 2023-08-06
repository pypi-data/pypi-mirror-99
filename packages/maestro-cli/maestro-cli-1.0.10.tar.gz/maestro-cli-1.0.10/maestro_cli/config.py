"""
Config for maestro cli
"""
import os
import sys

from ruamel.yaml import YAML

configuration_path = os.path.expanduser('~/.maestro.cfg')


try:
    yaml = YAML()
    with open(configuration_path, 'r') as stream:
        configuration = yaml.load(stream)
except IOError:
    configuration = {}


def get_setting(section, key):
    try:
        return configuration[section][key]
    except KeyError:
        sys.exit(
            "No section '%s.%s' in %s" %
            (section, key, configuration_path)
        )
