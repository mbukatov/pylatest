.. _xmlexport:

=====================
 Pylatest XML Export
=====================

Pylatest Sphinx extension also provides custom ``xmlexport`` `Sphinx builder`_
exporting test case documents into xml files for further machine processing
(scripting, reporting, transformation and/or importing somewhere else).

To generate xml export files, run ``make xmlexport`` (which runs
``$(SPHINXBUILD) -b xmlexport $(ALLSPHINXOPTS) $(BUILDDIR)/xmlexport``) in the
root directory of a Sphinx/Pylatest project.

XML Export file format
======================

XML export files are generated for test case documents only.

For the following example of minimal test case document:

.. code-block:: rst

    Hello World
    ***********

    :author: foo@example.com
    :caseimportance: low
    :casecomponent: foobar

    Description
    ===========

    This is just demonstration of usage of pylatest rst directives and expected
    structure of rst document.

    Test Steps
    ==========

    .. test_action::
       :step: List files in the volume: ``ls -a /mnt/helloworld``
       :result: There are no files, output should be empty.

XML Export file, using default configuration, would look
like this (example here has been little polished to increase readability
compared to actual xml export output):

.. code-block:: xml

    <?xml version='1.0' encoding='utf-8'?>
    <testcases>
      <testcase>
        <title>Hello World</title>
        <description>
          <html:div xmlns:html="http://www.w3.org/1999/xhtml" class="section" id="description">
          <html:p>This is just demonstration of usage of pylatest rst directives and expected
          structure of rst document.</html:p>
          </html:div>
        </description>
        <test-steps>
          <test-step>
            <test-step-column id="step">
              <html:div xmlns:html="http://www.w3.org/1999/xhtml" action_id="1" action_name="test_step" class="pylatest_action">
              List files in the volume: <html:code class="docutils literal"><html:span class="pre">ls</html:span> <html:span class="pre">-a</html:span> <html:span class="pre">/mnt/helloworld</html:span></html:code>
              </html:div>
            </test-step-column>
            <test-step-column id="expectedResult">
              <html:div xmlns:html="http://www.w3.org/1999/xhtml" action_id="1" action_name="test_result" class="pylatest_action">
              There are no files, output should be empty.
              </html:div>
            </test-step-column>
          </test-step>
        </test-steps>
        <custom-fields>
          <custom-field content="foobar" id="casecomponent"/>
          <custom-field content="low" id="caseimportance"/>
          <custom-field content="foo@example.com" id="author"/>
        </custom-fields>
      </testcase>
    </testcases>

Note that sections and test actions are represented as xhtml mixed content by
default.

Options for the XML Export builder
==================================

One can further tweak xml export behaviour by setting following options in
`conf.py build configuration file`_.

.. confval:: pylatest_project_id

    When specified, ``project-id`` attribute with given value is added into
    ``testcases`` element of xml export files.

.. confval:: pylatest_valid_export_metadata

    A list of test case metadata names (field names of field list entries used
    in rst files of test cases) which will be addedd into xml export file as
    ``custom-field`` element.

    When not specified, all test case metadata will be exported.

    For example of minimal test case document listed above, following
    configuration:

    .. code-block:: python

        pylatest_valid_export_metadata = [
            "casecomponent",
            "caseimportance",
            ]

    would prevent ``custom-field`` element for author to be included in xml
    export file, even though that author is specified in rst file of the test
    case and it would be present in standard html output.

.. confval:: pylatest_export_content_type

    Specifies how text content is included into xml elements of test case
    sections (*Description*, *Setup*, *Test Steps* and *Teardown*) in xml
    export file.

    Supported content types are:

    * ``mixedcontent``: content included as xhtml with proper xml namespace
      (aka *mixed xhtml content*) generated from rst source text of
      the section, see previous section for an example

    * ``CDATA``: content included as html code inside `CDATA section`_ (this
      is ugly hack and you should not use it)

    * ``plaintext``: plain text without any markup

    When not specified, ``mixedcontent`` is used.

    If you are not sure whether you should use ``CDATA`` option, use
    ``mixedcontent`` instead.

.. confval:: pylatest_export_pretty_print

    If False, xml export files would not be indented by lxml ``pretty_print``
    feature. Default is True.

    Note that xhtml mixed content sections (if enabled) are never indented, no
    matter how this option is set.

.. confval:: pylatest_export_lookup_method

    Controls how a test case is identified in xml export file.

    Supported options are:

    * ``custom``: test cases are identified by it's absolute *doc name* (path
      of rst file within sphinx project, without extension).

      For example, test case from file ``foo/test_bar.rst`` (file path within
      sphinx/pylatest project) will have it's id specified in attribute of
      test case element like this:

      .. code-block:: xml

          <testcase id="/foo/test_bar">

      Note that xml export file also declares the lookup method in it's
      properties:

      .. code-block:: xml

          <testcases>
            <properties>
              <property name="lookup-method" value="custom"/>

    * ``id``: value explicitelly specified as a test case id in rst file is
      directly used in it's xml export file. If a test case id is not provided
      in rst file, the xml element for the test case will be missing ``id``
      attribute.

      To explicitelly specify id for a test case, add ``:id:`` field into
      docutils field list with test case metadata:

      .. code-block:: rst

          Hello World
          ***********

          :id: FOO-123
          :author: foo@example.com
          :caseimportance: low
          :casecomponent: foobar

      Then the test case element in xml export file will just use this id:

      .. code-block:: xml

          <testcase id="FOO-123">

      Note that xml export file also declares the lookup method in it's
      properties:

      .. code-block:: xml

          <testcases>
            <properties>
              <property name="lookup-method" value="id"/>

    * ``id,custom``: a hybrid mode of the previous two. Custom id based on *doc
      name* is used, unless explicit id is specified in the rst file.

      The lookup method in property element of xml export file is set
      accordingly for each test case.

      Note that this is experimental feature, and may be changed or even
      removed in the future.

    When not specified, ``custom`` method is used.

.. confval:: pylatest_export_dry_run

    If True, xml export files will contain ``dry-run`` property set to
    ``true``:

    .. code-block:: xml

        <testcases>
          <properties>
            <property name="dry-run" value="true"/>

    This ``dry-run`` property element will be completelly missing when
    ``pylatest_export_dry_run`` is set to False.

    The default value is False.

.. confval:: pylatest_export_response_properties

    This config. option allows to specify a dict with properties to be included
    in xml export files as so called response properties.

    For example this dictionary:

    .. code-block:: python

        pylatest_export_response_properties = {
            "foo": "bar",
            "uuid": "5da60d66-916e-45fc-a6c6-edfba9444e54",
            }

    Will be represented as follows in xml export files:

    .. code-block:: xml

        <testcases>
          <response-properties>
            <response-property name="foo" value="bar"/>
            <response-property name="uid" value="5da60d66-916e-45fc-a6c6-edfba9444e54"/>

    This ``response-properties`` element won't be included in xml export files
    when the option is undefined.


.. _`Sphinx builder`: http://www.sphinx-doc.org/en/stable/builders.html
.. _`conf.py build configuration file`: http://www.sphinx-doc.org/en/stable/config.html
.. _`CDATA section`: https://en.wikipedia.org/wiki/CDATA
