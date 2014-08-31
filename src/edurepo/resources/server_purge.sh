#!/bin/sh
cd $HOME/git/edurepo
. envs/edurepo/bin/activate
cd src/edurepo
python resources/purge_links.py $*
