.. _xmlexport:

=====================
 Pylatest XML Export
=====================

To generate XML export files, run ``make clean`` and then ``make xmlexport``
(which runs ``$(SPHINXBUILD) -b xmlexport $(ALLSPHINXOPTS)
$(BUILDDIR)/xmlexport``) in the root directory of sphinx/pylatest project.

Executing ``make clean`` is required because of known issue with xml export
builder, which produces different doctree compared to html builder.

XML export file is generate for test case documents only.
