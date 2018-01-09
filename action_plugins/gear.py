# (c) 2015, Ansible Inc,
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        ''' handler for package operations '''

        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            # if we delegate, we should use delegated host's facts
            if self._task.delegate_to:
                module = self._templar.template("{{hostvars['%s']['gear_type']}}" % self._task.delegate_to)
            else:
                module = self._templar.template('{{gear_type}}')
        except:
            pass  # could not get it from template!

        if module not in self._shared_loader_obj.module_loader:
            result['failed'] = True
            result['msg'] = 'Could not find a module for %s.' % module
        else:
            # run the 'gear' module
            new_module_args = self._task.args.copy()
            display.vvvv("Running %s" % module)
            result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async_val))

        return result
