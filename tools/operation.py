from bacnet_driver import BACnetClient


def bacnet_obj_list(host_ip, port, device_ip, device_id):
    print("IN OPERATE")
    client = BACnetClient()
    if client.create(ip_address=host_ip, port=port):
        result = client.get_object_list(device_ip, device_id)
        client.disconnect()
        return result
    else:
        return False


def bacnet_whois(operate_dict):
    operate_dict['port'] = int(operate_dict['port'])
    client = BACnetClient()
    if client.create(ip_address=operate_dict['ip'], port=operate_dict['port']):
        result = client.who_is()
        client.disconnect()
        return result
    else:
        return False


def read_properties(*args):
    print('in oper prop')
    client = BACnetClient()
    if client.create(ip_address=args[0], port=args[1]):
        result = client.read_all_props(args[2], args[3], args[4])
        client.disconnect()
        return result
    else:
        return False
