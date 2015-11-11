Pylatest
========

Set of tools (docutils wrappers, custom rst directives) generating testcase
descriptions from source files written in reStructuredText.

Sphinx
------

To use pylatest directives in a sphinx project, you need to register them into
docutils rst parser in a similar way as it's done in ``pylatest2html``
command line client. Assuming you have pylatest installed properly (so that
you can import pylatest module without any problems), add following lines
into ``conf.py`` of your sphinx project::

    import pylatest.client

    pylatest.client.register_directives()

Development and testing
-----------------------

For instructions how to install pylatest from source code, see ``HACKING.rst``.
