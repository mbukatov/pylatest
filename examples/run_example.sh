#!/bin/bash
if [[ ! -d ../.env/bin ]]; then
  echo "create virtualenv first"
  exit 1
fi
source ../.env/bin/activate
cd ..
python setup.py install
cd -
# python -m pdb ../bin/pylatest2html.py --traceback test.rst
# pylatest2html.py --traceback test.rst
pylatest2html.py test.rst | tee test.html
