#!/bin/bash
ansible-playbook "$@" \
    --inventory=deploy_tools/ansible/hosts-staging \
    --private-key=~/.ssh/id_rsa \
    deploy_tools/ansible/site.yml
