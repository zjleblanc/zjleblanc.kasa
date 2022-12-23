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
        state: enabled
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

#### smart_dimmer

The smart_dimmer module can be used to find Kasa smart dimmers on your network and return useful information about them.

Examples:
```yaml
    - name: Get info about known smart dimmer
      zjleblanc.kasa.smart_dimmer:
        target: 192.168.0.100

    - name: Set alias for known smart dimmer
      zjleblanc.kasa.smart_dimmer:
        target: 192.168.0.100
        alias: Outdoor Dimming Lights

    - name: Turn on known smart dimmer
      zjleblanc.kasa.smart_dimmer:
        target: 192.168.0.100
        state: enabled
```

Output:
```json
{
    "changed": false,
    "smart_dimmer": {
        "alias": "Outdoor Dimming Lights",
        "brightness": 75,
        "host": "192.168.0.100",
        "hw_info": {
            "dev_name": "Wi-Fi Smart Dimmer",
            "hwId": "50B3F5C5DF12106A8C85E8903749DF1B",
            "hw_ver": "3.0",
            "mac": "6C:5A:B0:EE:8F:07",
            "mic_type": "IOT.SMARTPLUGSWITCH",
            "oemId": "774577CB2E1782A8BA53CDBBA136FAE6",
            "sw_ver": "1.0.3 Build 210202 Rel.190636"
        },
        "model": "HS220(US)",
        "on": false,
        "on_since": null,
        "type": "DeviceType.Dimmer"
    }
}
```