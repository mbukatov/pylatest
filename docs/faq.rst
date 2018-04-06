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

.. This particular combination of config options is tested during xml schema
   validation test case ``tests/xsphinx/test_export_schema_validation.py``.
   The values are specified in the following sphinx config file:
   ``tests/xsphinx/roots/test-export_schema_validation/conf.py``

Note that for ``pylatest_export_lookup_method`` you can use any valid method,
as long as the importer is configured accordingly.

It's also a good idea to restrict test case metadata which will be included in
the xml export file as ``custom-field`` elements by listing valid
field/metadata names in ``pylatest_valid_export_metadata``. This list should
contain only names which your ci-ops-tools xml importer accepts.

For more details, see :ref:`xmlexport`.
