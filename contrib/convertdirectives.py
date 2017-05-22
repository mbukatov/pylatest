#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
This script changes given rst document in place, converting old test action
directives ``test_step`` and ``test_result`` into ``test_action``.

It's a best effort hack, not an official part of pylatest (-: I realized that
such tool could be quite straighforward given already implemented pylatest
functionality, so here it is.
"""


import argparse

from pylatest.document import TestActions
from pylatest.rstsource import find_actions
from pylatest.xdocutils.core import register_all


parser = argparse.ArgumentParser(
    description="Convert directives test_{step,result} into test_action.")
parser.add_argument("rstfile")
args = parser.parse_args()

register_all(use_plain=True)

actions = TestActions()

# extract test actions of all deprecated test_{step,result} directives,
# including line numbers
with open(args.rstfile) as rstfile:
    rstsource = rstfile.read()
    for action in find_actions(rstsource):
        actions.add(action.action_name, action, action.action_id)

# list with content of rstfile
rstcontent = rstsource.splitlines()

# number of next line in rstfile to go to output, zero indexed
next_line_number = 0

with open(args.rstfile, "w") as rstfile:
    for action_id, test_step, test_result in actions:
        # make the assumptions clear
        assert test_step is not None
        assert test_step.start_line > next_line_number
        if test_result is not None:
            assert test_step.end_line < test_result.start_line
        # print all lines from last printed one to star of the current test_step
        for linenum in range(next_line_number, test_step.start_line - 1):
            print(rstcontent[linenum], file=rstfile)
        # convert test_step/test_result directive pair into test_action directive
        print(".. test_action::", file=rstfile)
        print("   :step:", file=rstfile)
        for linenum in range(test_step.start_line + 1, test_step.end_line):
            if len(rstcontent[linenum]) > 0:
                print("   " + rstcontent[linenum], file=rstfile)
            else:
                print(file=rstfile)
        next_line_number = test_step.end_line
        if test_result is not None:
            print("   :result:", file=rstfile)
            for linenum in range(test_result.start_line + 1, test_result.end_line):
                if len(rstcontent[linenum]) > 0:
                    print("   " + rstcontent[linenum], file=rstfile)
                else:
                    print(file=rstfile)
            next_line_number = test_result.end_line
    # ok, and now print the rest of the file
    for line in rstcontent[next_line_number:]:
        print(line, file=rstfile)
