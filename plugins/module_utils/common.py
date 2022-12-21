from kasa import SmartDevice, SmartDimmer

def get_device_info(device: SmartDevice):
    return {
        "alias": device.alias,
        "host": device.host,
        "model": device.model,
        "type": str(device.device_type),
        "hw_info": device.hw_info,
        "on": device.is_on
    }

def get_dimmer_info(dimmer: SmartDimmer):
    dimmer_info = get_device_info(dimmer)
    dimmer_info.update({
        "brightness": dimmer.brightness
    })
    return dimmer_info