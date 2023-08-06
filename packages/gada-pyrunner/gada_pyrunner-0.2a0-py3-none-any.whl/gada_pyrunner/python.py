"""Can run a gada node from a Python script by spawning a subprocess.

Basic Python package structure:

.. code-block:: bash

    ├── gadalang_mycomponent
    │   ├── __init__.py
    │   ├── mynode.py
    │   └── config.yml

Content of ``mynode.py``:

.. code-block:: python

    def main():
        print("hello world")

    if __name__ == "__main__":
        main()

Sample ``config.yml``:

.. code-block:: yaml

    nodes:
      mynode:
        runner: python
        file: mynode.py

Usage:

.. code-block:: bash

    $ gada mycomponent.mynode
    hello world

"""
__all__ = ["run"]
from typing import List, Optional
from gada.runners import generic


def run(comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None):
    """Run a gada node from a Python script.

    This will run the following command in a subprocess:

    .. code-block:: bash

        python ${file} ${argv}

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param kw: unused arguments
    """
    generic.run(
        comp=comp,
        gada_config=gada_config,
        node_config={
            "bin": node_config.get("bin", "python"),
            "file": node_config["file"],
            "env": node_config.get("env", {}),
        },
        argv=argv,
    )
