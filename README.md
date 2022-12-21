# Ansible Collection - zjleblanc.kasa

The kasa collection contains modules for automating [Kasa Smart](https://www.kasasmart.com/) devices.

## Content

### Modules

#### discover

The discover module can be used to find Kasa smart devices on your network and return useful information about them.

Example:
```yaml
    - name: Discover smart devices
      zjleblanc.kasa.discover:
```

Output:
```json
{
    "changed": true,
    "smart_devices": [
        {
            "alias": "Kitchen Lights",
            "host": "192.168.0.100",
            "hw_info": {
                "dev_name": "Smart Wi-Fi Light Switch",
                "hwId": "<id>",
                "hw_ver": "5.0",
                "mac": "<mac>",
                "mic_type": "IOT.SMARTPLUGSWITCH",
                "oemId": "<oem>",
                "sw_ver": "1.0.9 Build 221011 Rel.195547"
            },
            "model": "HS200(US)",
            "on": false,
            "type": "DeviceType.Plug"
        },
        ...
    ]
}
```

#### smart_device

The smart_device module can be used to find Kasa smart devices on your network and return useful information about them.

Examples:
```yaml
    - name: Get info about known smart device
      zjleblanc.kasa.smart_device:
        target: 192.168.0.100

    - name: Set alias for known smart device
      zjleblanc.kasa.smart_device:
        target: 192.168.0.100
        alias: Entryway Lights

    - name: Turn on known smart device
      zjleblanc.kasa.smart_device:
        target: 192.168.0.100
        state: on
```

Output:
```json
{
    "changed": true,
    "smart_device": [
        {
            "alias": "Kitchen Lights",
            "host": "192.168.0.100",
            "hw_info": {
                "dev_name": "Smart Wi-Fi Light Switch",
                "hwId": "<id>",
                "hw_ver": "5.0",
                "mac": "<mac>",
                "mic_type": "IOT.SMARTPLUGSWITCH",
                "oemId": "<oem>",
                "sw_ver": "1.0.9 Build 221011 Rel.195547"
            },
            "model": "HS200(US)",
            "on": true,
            "type": "DeviceType.Plug"
        }
    ]
}
```