#!/bin/sh

usage="Usage: $0 {prod|staging}"
if test $# -ne 1; then
    echo $usage 1>&2
    exit 1
fi

if test $1 != "prod"; then
    if test $1 != "staging"; then
        echo $usage 1>&2
        exit 1
    fi
fi

. ~/envs/ansible/bin/activate
exec ansible-playbook -i $HOME/server-config/$1/edurepo/ansible-settings deploy.yml
