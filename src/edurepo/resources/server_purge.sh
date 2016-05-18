#!/bin/sh
cd $HOME/git/edurepo
. envs/edurepo/bin/activate
export DJANGO_SETTINGS_MODULE=edurepo.settings
cd src/edurepo
python ./manage.py purge_resources --purge-stranded $*
