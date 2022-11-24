from flask import request
from operation import bacnet_whois, bacnet_obj_list, read_properties

# i_am_dict = {'device-ip': ['21', '22', '23'], 'device-id': [21, 22, 23], 'device_name': ['n1', 'n2', 'n3'],
#           'vendor': ['u', 'u', 'u']}

curr_device = {'ip': None, 'id': None}
bac_socket = {'ip': None, 'port': None}
curr_object = {'type': None, 'id': None}


def who_is():
    ipaddress = request.args.get("host-ip")
    port = request.args.get("port")
    bac_socket['ip'] = ipaddress
    bac_socket['port'] = port
    result = bacnet_whois(bac_socket)
    if isinstance(result, dict):
        return make_wi_response(result)
    else:
        return '<ol><li class="device">Not answer from devices</li></ol>'


def make_wi_response(devices):
    resp = '<div class="for-ol">'
    len_devices = len(devices['device-ip'])
    i = -1
    while i < (len_devices - 1):
        i += 1
        resp += (f'<p class="device">ID: {devices["device-id"][i]} IP: {devices["device-ip"][i]} '
                 f'NAME: {devices["device_name"][i]} VENDOR: {devices["vendor"][i]}</p>')
    resp += '</div>'
    return resp


def get_object_list():
    params = request.args.get("device").split(' ')
    curr_device['ip'] = params[3]
    curr_device['id'] = int(params[1])
    #   port = int(request.args.get("port"))
    #   host_ip = request.args.get("host-ip")
    result = bacnet_obj_list(bac_socket['ip'], bac_socket['port'], curr_device['ip'], curr_device['id'])
    if result:
        return make_obj_list_response(result)
    else:
        return '<ol><li>Something Wrong></li></ol>'


def make_obj_list_response(obj_list):
    resp = '<div class="for-ol">'
    len_objects = len(obj_list['type'])
    i = -1
    while i < (len_objects - 1):
        i += 1
        resp += f'<p class="object">{obj_list["type"][i]} {obj_list["id"][i]}</p>'
    resp += '</div>'
    return resp


def get_object_props():
    print('IN func prop')
    params = request.args.get("object").split(' ')
    curr_object['type'] = params[0]
    curr_object['id'] = params[1]
    result = read_properties(bac_socket['ip'], bac_socket['port'], curr_device['ip'], curr_object['type'], curr_object['id'])
    if result:
        response = ''
        res = str(result).split(',')
        for i in result:
            response += f"<p>{i}</p>"
        return response
    else:
        pass