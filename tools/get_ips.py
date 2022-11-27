import netifaces


def get_interfaces_ip():
    interfaces_list = list()
    got_interfaces = netifaces.interfaces()
    for i in got_interfaces:
        interface = netifaces.ifaddresses(i)
        if 2 in interface.keys():
            interface_ip = interface[2][0]['addr']
            interfaces_list.append(interface_ip)
    if len(interfaces_list) > 0:
        return interfaces_list

