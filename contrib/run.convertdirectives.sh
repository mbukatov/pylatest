#!/bin/bash
cd ~/projects/usmqe-testdoc
find . -name '*.rst' \
| xargs grep 'test_step' \
| cut -d: -f1 \
| sort \
| uniq \
| while read TCFILE; do
  ~/projects/pylatest/contrib/convertdirectives.py $TCFILE
  if [[ $? -ne 0 ]]; then
    echo $TCFILE >> convertdirectives.failed
    git checkout $TCFILE
  fi
done
