#!/bin/bash
if [[ ! -d ../.env/bin ]]; then
  echo "create virtualenv first"
  exit 1
fi
source ../.env/bin/activate
cd ..
python3 setup.py install
cd -
# python3 -m pdb ../bin/pylatest2html.py --traceback test.rst
# pylatest2html.py --traceback test.rst
pylatest2html.py test.rst | tee test.html
