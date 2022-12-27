#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import asyncio
from kasa import Discover, SmartDeviceException

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
        type: list
        elements: str
        default: []
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

- name: Get smart devices info
  zjleblanc.kasa.smart_device:
    target: 
        - 192.168.0.100
        - 192.168.0.101
        - 192.168.0.102

- name: Set smart device alias
  zjleblanc.kasa.smart_device:
    target: 192.168.0.100
    alias: "Backyard Lights"

- name: Turn smart device on
  zjleblanc.kasa.smart_device:
    target: 192.168.0.100
    state: enabled

- name: Turn smart devices off
  zjleblanc.kasa.smart_device:
    target: 
        - 192.168.0.100
        - 192.168.0.101
        - 192.168.0.102
    state: disabled
'''

RETURN = r'''
smart_devices:
    description: The target smart device info
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zjleblanc.kasa.plugins.module_utils.common import get_device_info

async def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        target=dict(type='list', required=True),
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

    alias = module.params['alias']
    state = module.params['state']
    mac = module.params['mac'] 
    targets = module.params['target']

    if not len(targets):
        module.fail_json('Must specify at least one target', **result)

    if len(targets) > 1 and (alias or mac):
        module.fail_json('Cannot set alias/mac for more than one device', **result)

    not_found = []
    smart_devices = {}
    for target in targets:
        try:
            dev = await Discover.discover_single(target)
            smart_devices[target] = dev
        except SmartDeviceException:
            not_found.append(target)

    if len(not_found):
        result['not_found'] = not_found
        module.fail_json('Failed to find at least one target', **result)

    for target in smart_devices:
        smart_device = smart_devices[target]
        await smart_device.update()
        original_state = get_device_info(smart_device)

        if alias:
            await smart_device.set_alias(alias)
        if mac:
            await smart_device.set_mac(mac)

        if state:
            if state == 'enabled':
                await smart_device.turn_on()
            elif state == 'disabled':
                await smart_device.turn_off()
        
        await smart_device.update()
        current_state = get_device_info(smart_device)
        result['smart_devices'][smart_device.host] = current_state
        result['changed'] = result['changed'] or (original_state != current_state)
        # Do not evaluate on_since as part of changed
        result['smart_devices'][smart_device.host]['on_since'] = smart_device.on_since

    module.exit_json(**result)


async def main():
    await run_module()


if __name__ == '__main__':
    asyncio.run(main())