"""A component is a bundle of nodes callable from gada.

Those nodes may be written in any language, but the component must be
a python package installed in site-packages.

All components must be python packages prefixed by gadalang_ to clearly
identify them.
"""
import os
from typing import Optional


def load(name: str):
    """Load a component installed in site-packages.

    This will raise an exception if no component is found.

    :param name: component name
    :return: component
    """
    try:
        import importlib

        return importlib.import_module(f"gadalang_{name}")
    except Exception as e:
        raise Exception(f"component {name} not found, verify it is installed") from e


def get_dir(comp) -> str:
    """Get the parent directory of a component.

    This is the same as:

    .. code-block:: python

        os.path.abspath(os.path.dirname(comp.__file__))

    :param comp: loaded component
    :return: parent directory
    """
    return os.path.abspath(os.path.dirname(comp.__file__))


def load_config(comp) -> dict:
    """Load a component configuration.

    This will raise an exception if the configuration is invalid.

    :param comp: component
    :return: config as dict
    """
    try:
        config_path = os.path.join(os.path.dirname(comp.__file__), "config.yml")

        with open(config_path, "r") as f:
            import yaml

            # Parse configuration
            config = yaml.safe_load(f.read())

            # yaml.safe_load returns None if file is empty
            return config if config is not None else {}
    except Exception as e:
        raise Exception("could not load component configuration") from e


def get_node_config(config: dict, node: str) -> dict:
    """Get a node configuration.

    :param config: component configuration
    :param node: node name
    :return: node configuration
    """
    nodes = config.get("nodes", [])
    if node not in nodes:
        raise Exception(f"no node {node} found in configuration")

    node_config = {
        "runner": config.get("runner", None),
        "cwd": config.get("cwd", None),
        "env": config.get("env", {}),
    }

    node_config.update(nodes[node])

    return node_config
