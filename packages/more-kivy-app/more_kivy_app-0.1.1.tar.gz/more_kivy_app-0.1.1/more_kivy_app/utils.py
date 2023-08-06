"""Utilities
=============
"""
from kivy.properties import ObservableDict, ObservableList, Property
from functools import partial
from tree_config.utils import yaml_loads as orig_yaml_loads,\
    get_yaml as orig_get_yaml, yaml_dumps as orig_yaml_dumps
from pathlib import Path

__all__ = ('get_yaml', 'yaml_dumps', 'yaml_loads')


def represent_property(representer, data: Property):
    return representer.represent_data(data.defaultvalue)


def get_yaml():
    yaml = orig_get_yaml()
    yaml.default_flow_style = False

    def represent_str(yml, val):
        return yaml.representer.__class__.represent_str(yml, str(val))

    yaml.representer.add_multi_representer(
        ObservableList, yaml.representer.__class__.represent_list)
    yaml.representer.add_multi_representer(
        ObservableDict, yaml.representer.__class__.represent_dict)
    yaml.representer.add_multi_representer(Path, represent_str)

    yaml.representer.add_multi_representer(Property, represent_property)
    return yaml


def yaml_loads(value, get_yaml_obj=get_yaml):
    # somehow in older versions, b'yuv420p' got encoded to
    # '!!binary |\neXV2NDIwcA==\n' instead of '!!binary |\n eXV2NDIwcA==\n'.
    # So now it can't be parsed. Hence add the space
    if len(value) >= 12 and value.startswith('!!binary |\n') and \
            value[11] != ' ':
        value = value[:11] + ' ' + value[11:]
    return orig_yaml_loads(value, get_yaml_obj=get_yaml_obj)


yaml_dumps = partial(orig_yaml_dumps, get_yaml_obj=get_yaml)
