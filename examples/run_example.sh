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
rm -f hello.*html

# python -m pdb ../bin/pylatest2html --traceback hello.rst
# pylatest2html --traceback hello.rst

# use hello.rst file
pylatest2html hello.rst | tee hello.html
pylatest2htmlplain hello.rst | tee hello.plain.html

# try to use default template
# pylatest-template --author john@example.com foobar
# pylatest2html foobar.rst | tee foobar.html
# pylatest2htmlplain foobar.rst | tee foobar.plain.html
