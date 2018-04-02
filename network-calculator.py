from Network import Network
import socket
import re
import sys


def get_network_with_subnet():
    if len(sys.argv) == 1:
        ip_address = socket.gethostbyname(socket.gethostname())
        first_octet = ip_address.split('.')[0]
        subnet_mask = 0
        if 1 <= int(first_octet) <= 126:
            subnet_mask = "8"
        elif 128 <= int(first_octet) <= 191:
            subnet_mask = "16"
        elif 192 <= int(first_octet) <= 223:
            subnet_mask = "24"

    else:
        ip_address = sys.argv[1].split('/')[0]
        subnet_mask = sys.argv[1].split('/')[1]
    match = re.match('^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}', ip_address)
    if match is None:
        print "Invalid IP address"
        sys.exit(2)
    for octet in ip_address.split('.'):
        if 0 > int(octet) > 255:
            print "Invalid IP address"
            sys.exit(2)
    if 0 > int(subnet_mask) > 32:
        print "Invalid subnet mask"
        sys.exit(2)
    ip_address += '/' + subnet_mask
    return ip_address


address = get_network_with_subnet()
network = Network(address)

network.generate_info()
