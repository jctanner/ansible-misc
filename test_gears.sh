#!/bin/bash
export SSH_AUTH_SOCK=0
ansible-playbook -vvvv -i inventory test_gears.yml
RC=$?
exit $RC
