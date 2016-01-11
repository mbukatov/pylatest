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
rm hello.html
rm hello.generated.rst

# python -m pdb ../bin/pylatest2html --traceback hello.rst
# pylatest2html --traceback hello.rst

# use hello.rst file
pylatest2html hello.rst | tee hello.html
pylatest2htmlplain hello.rst | tee hello.plain.html

# try to use default template
pylatest-template --author john@example.com foobar
pylatest2html foobar.rst | tee foobar.html
pylatest2htmlplain foobar.rst | tee foobar.plain.html

# try to generate rst file from python code, it should match hello.rst
py2pylatest hello.py > hello.generated.rst
diff hello.rst hello.generated.rst
