#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import os

GEARDIR = '/tmp/gears'
GEARNAME = 'sprocket'


def set_gear(gearname, filepath):
    with open(filepath, 'w') as f:
        f.write(gearname + '\n')


def unset_gear(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)


def run_module():

    gearfile = os.path.join(GEARDIR, '{}.txt'.format(GEARNAME))

    module_args = dict(
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not os.path.isdir(GEARDIR):
        module.fail_json(msg="The {} directory does not exist".format(GEARDIR))

    if module.params['state'] == 'present':
        if not os.path.isfile(gearfile):
            result['changed'] = True
            if not module.check_mode:
                set_gear(GEARNAME, gearfile)
    else:
        if os.path.isfile(gearfile):
            result['changed'] = True
            if not module.check_mode:
                unset_gear(gearfile)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
