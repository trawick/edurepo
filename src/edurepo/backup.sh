#!/bin/sh
cd $HOME/git/edurepo
. envs/edurepo/bin/activate
cd src/edurepo
python backup.py $*