#!/bin/bash
if [[ ! -d ../.env/bin ]]; then
  echo "create virtualenv first"
  exit 1
fi
source ../.env/bin/activate
cd ..
python setup.py install
cd -

# remove previous results
rm foobar.*
rm test.html

# python -m pdb ../bin/pylatest2html --traceback test.rst
# pylatest2html --traceback test.rst
pylatest2html test.rst | tee test.html

# try to use default template
pylatest-template --author john@example.com foobar
pylatest2html foobar.rst | tee foobar.html
