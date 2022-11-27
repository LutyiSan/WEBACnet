from bacnet_driver import BACnetClient
from time import sleep
from loguru import logger


def bacnet_obj_list(host_ip, port, device_ip, device_id):
    client = BACnetClient()
    if client.create(ip_address=host_ip, port=port):
        result = client.get_object_list(device_ip, device_id)
        if result:
            client.disconnect()
            sleep(0.3)
            return result
        else:
            client.disconnect()
            sleep(0.3)
    else:
        try:
            client.disconnect()
            sleep(0.3)
        except Exception as e:
            logger.exception(e)


def bacnet_whois(operate_dict):
    operate_dict['port'] = int(operate_dict['port'])
    client = BACnetClient()
    if client.create(ip_address=operate_dict['ip'], port=operate_dict['port']):
        result = client.who_is()
        if result:
            client.disconnect()
            sleep(0.3)
            return result
        else:
            client.disconnect()
            sleep(0.3)
    else:
        try:
            client.disconnect()
            sleep(0.3)
        except Exception as e:
            logger.exception(e)


def read_properties(*args):
    client = BACnetClient()
    if client.create(ip_address=args[0], port=args[1]):
        result = client.read_all_props(args[2], args[3], args[4])
        if result:
            client.disconnect()
            sleep(0.3)
            return result
        else:
            client.disconnect()
            sleep(0.3)
    else:
        try:
            client.disconnect()
            sleep(0.3)
        except Exception as e:
            logger.exception(e)


def read_property(*args):
    client = BACnetClient()
    if client.create(ip_address=args[0], port=args[1]):
        result = client.read_single(args[2], args[3], args[4], args[5])
        if result:
            client.disconnect()
            sleep(0.3)
            return result
        else:
            client.disconnect()
            sleep(0.3)
    else:
        try:
            client.disconnect()
            sleep(0.3)
        except Exception as e:
            logger.exception(e)
