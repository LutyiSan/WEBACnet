from BAC0.scripts.Lite import Lite
from validator import validate_ip
from loguru import logger


class BACnetClient:

    def create(self, ip_address: str, port: int) -> True or None:
        try:
            self.client = Lite(ip=ip_address, port=port)
            logger.debug("READY create bacnet-client")
            return True
        except Exception as e:
            logger.exception("FAIL create bacnet-client", e)

    def get_object_list(self, device_ip: str, device_id: int) -> dict or None:
        object_dict = {'type': [], 'id': []}
        try:
            object_list = self.client.read(f"{device_ip}/24 device {device_id} objectList")
            if len(object_list) > 0:
                for obj in object_list:
                    object_dict['type'].append(obj[0])
                    object_dict['id'].append(obj[1])
                return object_dict
        except Exception as e:
            logger.exception('Fail read object-list!', e)

    def who_is(self) -> dict or None:
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
        except Exception as e:
            logger.exception("NO RESPONSE WHO-IS", e)

    def read_single(self, device_ip: str, obj_type: str, obj_id: int, obj_property: str):
        try:
            prop = self.client.read(f'{device_ip}/24 {obj_type} {obj_id} {obj_property}')
            if prop:
                return prop
        except Exception as e:
            logger.exception(e)

    def read_all_props(self, device_ip, obj_type, obj_id):
        try:
            properties = self.client.readMultiple(f"{device_ip}/24 {obj_type} {obj_id} all")
            return properties
        except Exception as e:
            logger.exception(e)

    def disconnect(self) -> None:
        self.client.disconnect()
        logger.debug('CLIENT disconnected')
