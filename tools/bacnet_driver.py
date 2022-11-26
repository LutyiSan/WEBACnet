import BAC0
from BAC0.scripts.Lite import Lite
from loguru import logger
from validator import validate_ip, validate_digit


class BACnetClient:

    def create(self, ip_address: str, port: int) -> False:
        try:
            self.client = Lite(ip=ip_address, port=port)
            print("READY create bacnet-client")
            return True
        except Exception as e:
            print("FAIL create bacnet-client", e)

    def get_object_list(self, ip, id) -> dict or False:
        object_dict = {'type': [], 'id': []}
        try:
            object_list = self.client.read(f"{ip}/24 device {id} objectList")
            if len(object_list) > 0:
                for obj in object_list:
                    object_dict['type'].append(obj[0])
                    object_dict['id'].append(obj[1])
            return object_dict
        except Exception as e:
            print('Fail read object-list!', e)

    def who_is(self) -> dict or False:
        i_am_dict = {'device-ip': [], 'device-id': [], 'device_name': [], 'vendor': []}
        try:
            i_am_list = self.client.whois()
            if len(i_am_list) > 0:
                for device in i_am_list:
                    if validate_ip(device[0]):
                        i_am_dict['device-ip'].append(device[0])
                        i_am_dict['device-id'].append(device[1])
                        name = self.client.read(f'{device[0]}/24 device {device[1]} objectName')
                        vendor = self.client.read(f'{device[0]}/24 device {device[1]} vendorName')
                        if isinstance(name, (str, list)) and len(name) > 0:
                            i_am_dict['device_name'].append(name)
                        else:
                            i_am_dict['device_name'].append(None)
                        if isinstance(vendor, (str, list)) and len(vendor) > 0:
                            i_am_dict['vendor'].append(vendor)
                        else:
                            i_am_dict['vendor'].append(None)
                return i_am_dict
            else:
                return False
        except Exception as e:
            print("NO RESPONSE WHO-IS", e)

    def read_single(self, ip, type, id, property):
        print('PROPERTY to read', property)
        try:
            prop = self.client.read(f'{ip}/24 {type} {id} {property}')
            if prop:
                if property == 'statusFlags':
                    return sign_sf(prop)
                else:
                    return prop
            else:
                return 'none'
        except Exception as e:
            print(e)

    def read_all_props(self, ip, type, id):
        print("in bacnet prop")
        try:
            properties = self.client.readMultiple(f"{ip}/24 {type} {id} all")
            print(properties)
            return properties
        except Exception as e:
            print(e)

    def disconnect(self) -> None:
        self.client.disconnect()

    @staticmethod
    def rpm_maker(read_chunk: dict) -> dict or None:
        if not isinstance(read_chunk, dict):
            return None
        read_objects = dict()
        rpm = {'address': read_chunk['device-ip']}
        idx = -1
        while idx < (len(read_chunk["object-id"]) - 1):
            idx += 1
            key_0 = read_chunk['object-type'][idx]
            key_1 = read_chunk['object-id'][idx]
            properties = ['presentValue', 'statusFlags']
            read_objects.update({f"{key_0}:{key_1}": properties})
        rpm['objects'] = read_objects
        return rpm


def sign_sf(sf: any) -> list:
    print(sf)
    if not isinstance(sf, list):
        return [None, None, None, None]
    if sf is not None and len(sf) == 4:
        if sf[0] == 1:
            sf[0] = 'in-alarm'
        if sf[1] == 1:
            sf[1] = 'fault'
        if sf[2] == 1:
            sf[2] = 'overridden'
        if sf[3] == 1:
            sf[3] = 'out-of-service'
        print(sf)
        return sf
    else:
        return [None, None, None, None]


"""

 Example using
 ______________

    cl = BACnetClient()
    cl.create('192.168.1.67', 47808)
    cl.who_is()
    cl.get_object_list(device)
    cl.read_single(point)
    rpm = BACnetClient.rpm_maker(points)
    cl.read_multiple('192.168.1.82', rpm)
"""
