#!/bin/bash
source ../.env/bin/activate
cd ..
python setup.py install
cd -
# python -m pdb ../bin/pylahello.py --traceback hello.rst
pylahello.py --traceback hello.rst
