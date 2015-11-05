#!/bin/bash
source ../.env/bin/activate
cd ..
python3 setup.py install
cd -
# python3 -m pdb ../bin/pylahello.py --traceback hello.rst
# pylahello.py --traceback hello.rst
pylahello.py hello.rst | tee hello.html
