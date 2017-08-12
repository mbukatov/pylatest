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

.. note:: Workaround is required

    Executing ``make clean`` before running ``make xmlexport`` is needed
    because of known problem with Pylatest xml export builder, which produces
    different doctree compared to standard html builder.

    For the same reason, one have to run ``make clean`` again before building
    html (or any other than ``xmlexport``) output.

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

    * ``plaintext``: plain text without any markup

    When not specified, ``mixedcontent`` is used.

.. confval:: pylatest_export_pretty_print

    If False, xml export files would not be indented by lxml ``pretty_print``
    feature. Default is True.

    Note that xhtml mixed content sections (if enabled) are never indented, no
    matter how this option is set.


.. _`Sphinx builder`: http://www.sphinx-doc.org/en/stable/builders.html
.. _`conf.py build configuration file`: http://www.sphinx-doc.org/en/stable/config.html
