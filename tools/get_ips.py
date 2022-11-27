import netifaces


def get_interfaces_ip():
    interfaces = list()
    n = netifaces.interfaces()
    for i in n:
        inn = netifaces.ifaddresses(i)
        if 2 in inn.keys():
            interface_ip = inn[2][0]['addr']
            interfaces.append(interface_ip)
            print(interface_ip)
    if len(interfaces) > 0:
        return interfaces
    else:
        return 'No interfaces in device'
