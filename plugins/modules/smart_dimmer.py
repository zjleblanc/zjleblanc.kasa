#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import asyncio
from kasa import Discover, DeviceType, SmartDeviceException

DOCUMENTATION = r'''
---
module: smart_dimmer

short_description: Automate kasa smart devices with dimming capabilities

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Use this module to automate Kasa smart devices with dimming capabilities in your home or business.

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
    brightness:
        description: The desired brightness of the smart device
        required: false
        type: int
    transition:
        description: Transition time to desired brightness (ms)
        required: false
        type: int
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
- name: Get smart dimmer info
  zjleblanc.kasa.smart_dimmer:
    target: 192.168.0.100

- name: Set smart dimmer alias
  zjleblanc.kasa.smart_dimmer:
    target: 192.168.0.100
    alias: "Backyard Lights"

- name: Turn smart dimmer on
  zjleblanc.kasa.smart_dimmer:
    target: 192.168.0.100
    state: enabled
    brightness: 50
    transition: 100

- name: Turn smart dimmers off
  zjleblanc.kasa.smart_dimmer:
    target: 
        - 192.168.0.100
        - 192.168.0.101
        - 192.168.0.102
    state: disabled
    transition: 100
'''

RETURN = r'''
smart_dimmers:
    description: The target smart dimmer info
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zjleblanc.kasa.plugins.module_utils.common import get_dimmer_info

async def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        target=dict(type='str', required=True),
        state=dict(type='str', required=False, default=None),
        brightness=dict(type='int'),
        transition=dict(type='int'),
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
    brightness = module.params['brightness']
    transition = module.params['transition']

    if not len(targets):
        module.fail_json('Must specify at least one target', **result)
    if brightness and (brightness < 0 or brightness > 100):
        module.fail_json('Invalid brightness: must be [0-100]', **result)
    if len(targets) > 1 and (alias or mac):
        module.fail_json('Cannot set alias/mac for more than one device', **result)

    not_found = []
    smart_dimmers = {}
    for target in targets:
        try:
            dimmer = await Discover.discover_single(target)
            smart_dimmers[target] = dimmer
            if dimmer.device_type != DeviceType.Dimmer:
                raise SmartDeviceException()
        except SmartDeviceException:
            not_found.append(target)

    if len(not_found):
        result['not_found'] = not_found
        module.fail_json('Failed to find at least one target dimmer', **result)

    for target in smart_dimmers:
        smart_dimmer = smart_dimmers[target]
        await smart_dimmer.update()
        original_state = get_dimmer_info(smart_dimmer)

        if alias:
            await smart_dimmer.set_alias(alias)
        if mac:
            await smart_dimmer.set_mac(mac)
        if brightness:
            await smart_dimmer.set_brightness(brightness)
        if state:
            if state == 'enabled':
                await smart_dimmer.turn_on(transition=transition)
            elif state == 'disabled':
                await smart_dimmer.turn_off(transition=transition)
        
        await smart_dimmer.update()
        current_state = get_dimmer_info(smart_dimmer)
        result['smart_dimmers'][smart_dimmer.host] = current_state
        result['changed'] = result['changed'] or (original_state != current_state)
        result['smart_dimmers'][smart_dimmer.host]['on_since'] = smart_dimmer.on_since

    module.exit_json(**result)


async def main():
    await run_module()


if __name__ == '__main__':
    asyncio.run(main())