#!/bin/sh

PROJECT=edurepo

usage="Usage: $0 {prod|staging} [ansible-options]"
if test $# -lt 1; then
    echo $usage 1>&2
    exit 1
fi

SERVER=$1
shift

if test $SERVER != "prod"; then
    if test $SERVER != "staging"; then
        echo $usage 1>&2
        exit 1
    fi
fi

. ~/envs/ansible/bin/activate
exec ansible-playbook $* -i $HOME/server-config/${SERVER}/${PROJECT}/ansible-settings deploy.yml
