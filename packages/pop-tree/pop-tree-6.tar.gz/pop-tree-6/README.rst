********
POP-TREE
********
**POP hub and sub visualization tool**

INSTALLATION
============

Bare installation with no dependencies

.. code-block:: bash

    pip install pop-tree

Installation for pretty yaml output

.. code-block:: bash

    pip install pop-tree\[rend\]

Installation for incredible graphs

.. code-block:: bash

    pip install pop-tree\[networkx\]

Install everything

.. code-block:: bash

    pip install pop-tree\[full\]

INSTALLATION FOR DEVELOPMENT
============================

Clone the `pop-tree` repo and install with pip


.. code-block:: bash

    git clone https://gitlab.com/Akm0d/pop-tree.git
    pip install -e pop-tree\[full\]

EXECUTION
=========

After installation the `pop-tree` command should now be available.

Running `pop-tree` by itself will only show things that the `pop-tree` project added to the hub.
Naming a dynamic namespace will add it's dyne_name to the hub and show only that namespace

.. code-block:: bash

    pop-tree exec

RECURSE
-------

Adding the `--recurse` flag will recursively load all subs underneath the named dynamic namespace (in the first positional arugment)

.. code-block:: bash

    pop-tree exec --recurse

ADD_SUB
-------

Every positional argument after `--add-sub` will be added as a `dyne_name` to the `hub`

Example

.. code-block:: bash

    pop-tree --add-sub idem grains

OUTPUT
------

If you installed pop-tree with the [rend] extras, then `--output` can be used to specify an outputter from the `rend` project
To see which outputters are available, just run

.. code-block:: bash

    pop-tree output

Which will dynamically load the `output` dynamic namespace from the `rend` project and print the subs loaded immediately beneath it.

.. code-block:: bash

    pop-tree --output nested

GRAPH
-----

There are many different graphing plugins, some print to the terminal, and some open a shiny graph in a new window.
To list the available graphing plugins, run

.. code-block:: bash

    pop-tree graph

A graph plugin can be specified with the `--graph` option.

.. code-block:: bash

    pop-tree --graph networkx

Which should print off a beautiful matplotlib plot to visualize your pop ecosystem.
Use these arguments together to create impressive visuals for your project.

.. image:: hub.png
