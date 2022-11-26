import BAC0
from BAC0.scripts.Lite import Lite
from loguru import logger
from validator import validate_ip, validate_digit


class BACnetClient:
    bc_logger = logger
    object_types = ['analogInput', 'analogOutput', 'analogValue', 'binaryInput', 'binaryOutput', 'binaryValue',
                    'multiStateInput', 'multiStateOutput', 'multiStateValue']

    def create(self, ip_address: str, port: int) -> False:
        if not validate_ip(ip_address):
            self.bc_logger.error('IP-address incorrect!')
            return False
        if not validate_digit(port, 1, 65535):
            self.bc_logger.error('Port number incorrect!')
            return False
        try:
            self.client = Lite(ip=ip_address, port=port)
            logger.debug("READY create bacnet-client")
            return True
        except Exception as e:
            logger.exception("FAIL create bacnet-client", e)
            return False

    def get_object_list(self, ip, id) -> dict or False:
        print("IN BACNET")
        object_dict = {'type': [], 'id': []}
        try:
            object_list = self.client.read(
                f"{ip}/24 device {id} objectList")
            if len(object_list) > 0:
                for obj in object_list:
                    object_dict['type'].append(obj[0])
                    object_dict['id'].append(obj[1])
            print(object_dict)
            return object_dict
        except Exception as e:
            self.bc_logger.exception('Fail read object-list!', e)
            return False

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
            self.bc_logger.exception("NO RESPONSE WHO-IS", e)
            return False

    def read_single(self, ip, type, id, property):
        try:
            prop = self.client.read(f'{ip}/24 {type} {id} {property}')
            if prop:
                return prop
            else:
                return 'none'
        except Exception as e:
            print(e)
            return 'none'



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

    @staticmethod
    def sign_sf(sf: any) -> list:
        if not isinstance(sf, list):
            return [None, None, None, None]
        if sf is not None and len(sf) == 4:
            if sf[0] and sf[0]:
                sf[0] = 'in-alarm'
            if sf[1] and sf[1]:
                sf[1] = 'fault'
            if sf[2] and sf[2]:
                sf[2] = 'overridden'
            if sf[3] and sf[3]:
                sf[3] = 'out-of-service'
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


