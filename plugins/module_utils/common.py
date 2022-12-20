from kasa import SmartDevice

def get_device_info(device: SmartDevice):
    return {
        "alias": device.alias,
        "host": device.host,
        "model": device.model,
        "type": str(device.device_type),
        "hw_info": device.hw_info,
        "on": device.is_on
    }