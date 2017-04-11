# -*- coding: utf8 -*-


from pylatest.xsphinx.extension import setup as sphinx_setup


# This makes it possible to refer to *Pylatest Sphinx plugin module* as just
# ``pylatest`` no matter where the actuall module with the plugin is located
def setup(app):
    return sphinx_setup(app)
