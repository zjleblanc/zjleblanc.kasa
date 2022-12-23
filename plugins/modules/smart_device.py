#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import asyncio
from kasa import Discover, DeviceType

DOCUMENTATION = r'''
---
module: smart_device

short_description: Automate kasa smart devices

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Use this module to automate Kasa smart devices in your home or business.

options:
    target:
        description: The target ip address for the smart device
        required: true
        type: str
    state:
        description: The desired state of the smart device
        required: false
        type: str
        choices:
            - enabled
            - disabled
            - updated
    alias:
        description: The smart device alias (as shown in Kasa app).
        required: false
        type: str
    mac:
        description: The smart device mac address.
        required: false
        type: str

author:
    - Zach LeBlanc (@zjleblanc)
'''

EXAMPLES = r'''
- name: Get smart device info
  zjleblanc.kasa.smart_device:
    target: 192.168.0.100

- name: Set smart device alias
  zjleblanc.kasa.smart_device:
    target: 192.168.0.100
    alias: "Backyard Lights"

- name: Turn smart device on
  zjleblanc.kasa.smart_device:
    target: 192.168.0.100
    state: enabled
'''

RETURN = r'''
smart_device:
    description: The target smart device info
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zjleblanc.kasa.plugins.module_utils.common import get_device_info

async def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        target=dict(type='str', required=True),
        state=dict(type='str', required=False, default=None),
        alias=dict(type='str', required=False, default=None),
        mac=dict(type='str', required=False, default=None)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    smart_device = await Discover.discover_single(module.params['target'])
    await smart_device.update()

    if smart_device.device_type == DeviceType.Unknown:
        module.fail_json('Smart device not found at target %s' % module.params['target'], **result)

    original_state = get_device_info(smart_device)

    if module.params['alias']:
        await smart_device.set_alias(module.params['alias'])

    if module.params['mac']:
        await smart_device.set_mac(module.params['mac'])

    desired_state = module.params['state']
    if module.params['state']:
        if desired_state == 'enabled':
            await smart_device.turn_on()
        elif desired_state == 'disabled':
            await smart_device.turn_off()
    
    await smart_device.update()
    result['smart_device'] = get_device_info(smart_device)
    result['changed'] = original_state != result['smart_device']
    result['smart_device']['on_since'] = smart_device.on_since
    module.exit_json(**result)


async def main():
    await run_module()


if __name__ == '__main__':
    asyncio.run(main())