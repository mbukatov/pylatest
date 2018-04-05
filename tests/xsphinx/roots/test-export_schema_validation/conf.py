# -*- coding: utf-8 -*-

extensions = ['pylatest']
master_doc = 'index'

# set of config options useful for ci-ops-tools xml importer, as mentioned in
# docs/faq.rst file
pylatest_project_id = "c954c159-75b9-46c6-9211-2a58acf521b8"
pylatest_export_content_type = "CDATA"
pylatest_export_lookup_method = "custom"

# some additional options (to cover more cases here)
pylatest_export_pretty_print = False
pylatest_export_dry_run = True
pylatest_export_response_properties = {
    "foo": "bar",
    "uuid": "5da60d66-916e-45fc-a6c6-edfba9444e54",
    }
