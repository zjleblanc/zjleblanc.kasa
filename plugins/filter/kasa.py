#!/usr/bin/python

class FilterModule(object):
    def filters(self):
        return {
            'kasa_host': self.get_kasa_host,
        }

    def get_kasa_host(self, smart_devices, alias):
        for dev in smart_devices:
            if dev['alias'] == alias:
                return dev['host']
        return None