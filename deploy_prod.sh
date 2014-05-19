#!/bin/bash
ansible-playbook "$@" \
    --inventory=deploy_tools/ansible/production \
    --private-key=~/.ssh/id_rsa \
    deploy_tools/ansible/site.yml
