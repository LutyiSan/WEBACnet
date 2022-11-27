from flask import request
from operation import bacnet_whois, bacnet_obj_list, read_properties, read_property
from tools.obj_props import obj_dict

curr_device = dict()
bac_socket = dict()
curr_object = dict()


def who_is():
    ipaddress = request.args.get("host-ip")
    port = request.args.get("port")
    bac_socket['ip'] = ipaddress
    bac_socket['port'] = port
    result = bacnet_whois(bac_socket)
    if isinstance(result, dict):
        return make_wi_response(result)
    else:
        return '<p>Not answer from devices</p>'


def make_wi_response(devices):
    resp = '<div>'
    i = -1
    while i < (len(devices['device-ip']) - 1):
        i += 1
        image = 'static/icons/device-icon.svg'
        resp += f"<p class='device'><img src='{image}'> ID: {devices['device-id'][i]} IP: {devices['device-ip'][i]}" \
                f" NAME: {devices['device_name'][i]} VENDOR: {devices['vendor'][i]}</p>"
    resp += '</div>'
    return resp


def get_object_list():
    params = request.args.get("device").split(' ')
    curr_device['ip'] = params[4]
    curr_device['id'] = int(params[2])
    result = bacnet_obj_list(bac_socket['ip'], bac_socket['port'], curr_device['ip'], curr_device['id'])
    if result:
        return make_obj_list_response(result)
    else:
        return '<p>No answer from device></p>'


def make_obj_list_response(obj_list):
    resp = '<div class="for-ol">'
    len_objects = len(obj_list['type'])
    i = -1
    while i < (len_objects - 1):
        i += 1
        if "Input" in obj_list["type"][i]:
            image = 'static/icons/in_obj.svg'
        elif "Output" in obj_list["type"][i]:
            image = 'static/icons/out_obj.svg'
        else:
            image = 'static/icons/value_obj.svg'
        resp += f'<p class="object"><img src="{image}"> {obj_list["type"][i]} {obj_list["id"][i]}</p>'
    resp += '</div>'
    return resp


def get_object_props():
    params = request.args.get("object").split(' ')
    curr_object['type'] = params[1]
    curr_object['id'] = params[2]
    if curr_object['type'] not in obj_dict.keys():
        result = read_properties(bac_socket['ip'], bac_socket['port'], curr_device['ip'], curr_object['type'],
                                 curr_object['id'])
        if result:
            response = ''
            for i in result:
                response += f"<p>{i}</p>"
            return response
        else:
            return '<p>Something Wrong></p>'
    else:
        return property_form()


def property_form():
    image = 'static/icons/property-icon.svg'
    response_head = '<div class="form"><p>Choose property</p>'
    properties = obj_dict[curr_object['type']]
    for i in properties:
        response_head += f"<p class='property' value='{i}'><img src='{image}'> {i}</p>"
    response_head += "</div> "
    return response_head


def read_select_properties():
    curr_object['property'] = request.args.get("property")
    result = read_property(bac_socket['ip'], bac_socket['port'], curr_device['ip'], curr_object['type'],
                           curr_object['id'], curr_object['property'])
    return f"<p>Property PV</p><p>{curr_object['property']}: {result}</p>"
