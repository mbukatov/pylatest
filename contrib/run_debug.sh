#!/bin/bash

# make sure we run this under virtualenv
if [[ ${VIRTUAL_ENV} ]]; then
  echo "looks like we are running in virtualenv: ${VIRTUAL_ENV}"
elif [[ -d ../.env/bin ]]; then
  source ../.env/bin/activate || exit 1
else
  echo "running outside of virtualenv, you need to create one"
  exit 1
fi

cd ..
python setup.py install
# fail immediately when installation breaks
if [[ $? -ne 0 ]]; then
  echo "setup.py failed"
  exit 2
fi
cd -

# remove previous results
rm -f *html

# to add break point somewhere:
# import pdb; pdb.set_trace()

# pylatest2html --traceback hello.rst
python -m pdb $(which pylatest2html) --traceback hello.rst
