from BAC0.scripts.Lite import Lite
from loguru import logger
from validator import validate_ip, validate_digit, validate_in_enum


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

    def read_single(self, point: dict) -> dict or False:
        if not isinstance(point, dict):
            return False
        result_dict = dict()
        if not validate_ip(point['device_ip']):
            self.bc_logger.error('IP-address incorrect!')
            return False
        if not validate_in_enum(self.object_types, point['obj_type']):
            self.bc_logger.error('Object TYPE incorrect!')
            return False
        if not validate_digit(point['obj_id'], 0, 4194303):
            self.bc_logger.error('Object ID incorrect!')
            return False
        try:
            self.present_value = self.client.read(f"{point['device_ip']}/24 {point['obj_type']}"
                                                  f" {point['obj_id']} presentValue")
            if isinstance(self.present_value, (int, float, str)):
                result_dict['present-value'] = [self.present_value]
            else:
                result_dict['present-value'] = [None]
            self.status_flags = self.client.read(f"{point['device_ip']}/24 {point['obj_type']}"
                                                 f" {point['obj_id']} statusFlags")
            if isinstance(self.status_flags, list) and len(self.status_flags) == 4:
                sf = BACnetClient.sign_sf(self.status_flags)
                result_dict['status-flags'] = sf
            else:
                result_dict['status-flags'] = [None, None, None, None]
            self.reliability = self.client.read(f"{point['device_ip']}/24"
                                                f" {point['obj_type']}"
                                                f" {point['obj_id']} reliability")
            if isinstance(self.reliability, str) and len(self.reliability) > 0:
                result_dict['reliability'] = [self.reliability]
            else:
                result_dict['reliability'] = [None]
            return result_dict
        except Exception as e:
            result_dict['present-value'] = [None]
            result_dict['status-flags'] = [None, None, None, None]
            result_dict['reliability'] = [None]
            self.bc_logger.exception('FAIL read object', e)
            return result_dict

    def read_multiple(self, device_ip: str, rpm: dict) -> dict or False:
        result_dict = {'present-value': [], 'status-flags': []}  # TODO property reliability
        if not validate_ip(device_ip):
            self.bc_logger.error('IP-address incorrect!')
            return False
        if not isinstance(rpm, dict):
            self.bc_logger.error('RPM-format  incorrect!')
            return False
        try:
            read_result = self.client.readMultiple(f'{device_ip}/24', request_dict=rpm)
            if len(read_result) == len(rpm['objects']):
                for i in read_result:
                    pv = read_result[i][0][1]
                    sf = read_result[i][1][1]
                    if pv == 'active':
                        result_dict["present-value"].append(True)
                    elif pv == 'inactive':
                        result_dict["present-value"].append(False)
                    else:
                        result_dict["present-value"].append(pv)
                    if sf is None:
                        result_dict["status-flags"].append([None, None, None, None])
                    else:
                        signed_sf = BACnetClient.sign_sf(sf)
                        result_dict["status-flags"].append(signed_sf)
            else:
                logger.error("FAIL MULTIPLE-READ")
                for _ in rpm['object-id']:
                    result_dict["present-value"].append(None)
                    result_dict["status-flags"].append(None)
                return result_dict
        except Exception as e:
            self.bc_logger.exception("FAIL MULTIPLE-READ", e)
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

