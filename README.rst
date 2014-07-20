pm 0.1.1
========

Simple project manager in Python. This application helps you keeping track of
the status of your projects in their Source Code Management (SCM) system. 

For now, pm only supports Git. 

Normally, it should be compatible with Python 2.7 and Python 3.x. Post an issue
if you find something that is not compatible one of these versions and I'll do
my best to improve that.

Installation
------------

You can use *pip* to install the latest *pm* release from PyPI::

    pip install pm

Alternatively, you can download the latest development sources and
install the package manually by running::

    python setup.py install

Usage
-----

Help can be obtained by running :code:`pm --help` to obtain information about
the general usage or :code:`pm <subcommand> --help` to obtain help about a
specific subcommand.

.. code::

    usage: pm [-h] [--version] {status,ls,fetch,update} ...

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

    subcommands:
      Valid subcommands

      {status,ls,fetch,update}
                            Subcommands
        status              check status
        ls                  List projects
        fetch               Fetch all projects
        update              Update all projects

License
-------

This project is distributed under the MIT License. Read *LICENSE* for details.
