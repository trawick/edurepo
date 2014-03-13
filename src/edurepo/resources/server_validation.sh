cd $HOME/git/edurepo
. envs/edurepo/bin/activate
cd src/edurepo
python resources/validate_links.py $*
