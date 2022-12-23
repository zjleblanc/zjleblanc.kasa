#!/usr/bin/python

# Copyright: (c) 2022, Zach LeBlanc <zjleblanc3@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import asyncio
from kasa import Discover

DOCUMENTATION = r'''
---
module: discover

short_description: Discover kasa smart devices

version_added: "1.0.0"

options:
    target:
        description: The target address where to send the broadcast discovery queries if multi-homing (e.g. 192.168.xxx.255)
        required: false
        type: str
        default: 255.255.255.255
    timeout:
        description: How long to wait for responses
        required: false
        type: int
        default: 5
    discovery_packets:
        description: Number of discovery packets to broadcast
        required: false
        type: int
        default: 3
    interface:
        description: Bind to specific interface
        required: false
        type: str
        default: None

author:
    - Zach LeBlanc (@zjleblanc)
'''

EXAMPLES = r'''
- name: Discover Kasa smart devices on network
  zjleblanc.kasa.discover:

- name: Discover Kasa smart device with particular IP
  my_namespace.my_collection.my_test:
    target: 192.168.0.100
'''

RETURN = r'''
smart_devices:
    description: The discovered Kasa smart devices
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zjleblanc.kasa.plugins.module_utils.common import get_device_info

async def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        target=dict(type='str', required=False, default='255.255.255.255'),
        timeout=dict(type='int', required=False, default=5),
        discovery_packets=dict(type='int', required=False, default=3),
        interface=dict(type='str', required=False, default=None)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    found_devices = await Discover.discover(
        target=module.params['target'], 
        on_discovered=None, timeout=module.params['timeout'], 
        discovery_packets=module.params['discovery_packets'], 
        interface=module.params['interface']
    )
    smart_devices = [dev[1] for dev in found_devices.items()]
    result['smart_devices'] = list(map(get_device_info, smart_devices))

    if len(result['smart_devices']) > 0:
        result['changed'] = True

    module.exit_json(**result)


async def main():
    await run_module()


if __name__ == '__main__':
    asyncio.run(main())