"""Can run a gada node from a Python package installed in ``PYTHONPATH`` without spawning a subprocess.

Basic Python package structure:

.. code-block:: bash

    ├── gadalang_mycomponent
    │   ├── __init__.py
    │   ├── mynode.py
    │   └── config.yml

Content of ``mynode.py``:

.. code-block:: python

    def main(**kwargs):
        print("hello world")

Sample ``config.yml``:

.. code-block:: yaml

    nodes:
      mynode:
        runner: pymodule
        module: gadalang_mycomponent.mynode
        entrypoint: main

Usage:

.. code-block:: bash

    $ gada mycomponent.mynode
    hello world

"""
__all__ = ["run"]
from typing import List, Optional


def load_module(name: str):
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:
        raise Exception(f"failed to import module {name}") from e


def run(
    comp,
    *,
    gada_config: dict,
    node_config: dict,
    argv: Optional[List] = None,
    **kw: dict,
):
    """Run a gada node from a Python package.

    This will load the module into memory and call the configured entrypoint:

    .. code-block:: python

        m = importlib.import_module[node_config["module"]]
        e = getattr(m, node_config["entrypoint"])
        e(...)

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param kw: unused arguments
    """
    argv = argv if argv is not None else []

    # Check the entrypoint is configured
    entrypoint = node_config.get("entrypoint", None)
    if not entrypoint:
        raise Exception("missing entrypoint in configuration")

    # Load module if explicitely configured
    if "module" in node_config:
        comp = load_module(node_config["module"])

    # Check the entrypoint exists
    fun = getattr(comp, entrypoint, None)
    if not fun:
        raise Exception(f"module {comp.__name__} has no entrypoint {entrypoint}")

    # Call entrypoint
    fun(argv=[comp.__name__] + argv)
