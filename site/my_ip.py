import netifaces as ni


def gei_ip(interface_name='{CB37E1E8-2571-4D3A-9B12-001AABE13FE5}'):
    return ni.ifaddresses(interface_name)[ni.AF_INET][0]['addr']

print(gei_ip())
