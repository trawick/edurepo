#!/bin/sh
cd $HOME/git/edurepo
. envs/edurepo/bin/activate
cd src/edurepo
python teachers/pretend_teacher.py $*
