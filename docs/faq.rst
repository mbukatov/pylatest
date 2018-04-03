.. _faq:

============================
 Frequently Asked Questions
============================

How to configure Sphinx/Pylatest project for ci-ops-tools xml importer?
=======================================================================

If you need to use xml export files (generated via ``make xmlexport``) with
ci-ops-tools xml importer, you will need to use the following configuration in
``conf.py`` file of your project:

.. code-block:: python

    pylatest_project_id = "SOME-ID-IMPORTER-ALREADY-RECOGNIZES"
    pylatest_export_content_type = "CDATA"
    pylatest_export_lookup_method = "custom"

Note that for ``pylatest_export_lookup_method`` you can use any valid method,
as long as the importer is configured accordingly.

For more details, see :ref:`xmlexport`.
