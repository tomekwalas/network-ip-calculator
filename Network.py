import json


def to_binary(address):
    binaryAddress = []
    for octet in address:
        binaryAddress.append(format(octet, '08b'))
    return binaryAddress


def decrement_address(address):
    tmpAddress = list(reversed(address))
    for i, e in enumerate(tmpAddress):
        if e == 0:
            tmpAddress[i] = 255
        else:
            tmpAddress[i] = e - 1
            return list(reversed(tmpAddress))


def increment_address(address):
    tmpAddress = list(reversed(address))
    for i, e in enumerate(tmpAddress):
        if e == 255:
            tmpAddress[i] = 0
        else:
            tmpAddress[i] = e + 1
            return list(reversed(tmpAddress))


class Network:
    subnet_mask = [0, 0, 0, 0]
    ip_address = []
    nbits = 0
    network_class = ''
    hosts_number = 0
    subnet_number = 0

    def __init__(self, address):
        addr = address.split('/')[0]
        nbit = address.split('/')[1]

        self.ip_address = [int(x) for x in addr.split('.')]
        self.nbits = int(nbit)
        self.get_network_class()
        self.calculate_default_address()
        self.calculate_subnet_mask()
        self.calculate_hosts_number()
        self.calculate_subnets_number()
        pass

    def get_network_class(self):
        first_octet = self.ip_address[0]
        if 1 <= first_octet <= 126:
            self.network_class = 'A'
        elif 128 <= first_octet <= 191:
            self.network_class = "B"
        elif 192 <= first_octet <= 223:
            self.network_class = "C"
        elif 224 <= first_octet <= 239:
            self.network_class = "D"
        elif 240 <= first_octet <= 255:
            self.network_class = "E"

    def calculate_default_address(self):
        if self.network_class == "A":
            self.ip_address[1] = self.ip_address[2] = self.ip_address[3] = 0
        elif self.network_class == "B":
            self.ip_address[2] = self.ip_address[3] = 0
        elif self.network_class == "C":
            self.ip_address[3] = 0
        pass

    def calculate_subnet_mask(self):
        for i in range(self.nbits):
            self.subnet_mask[i / 8] += 1 << (7 - i % 8)
        pass

    def calculate_hosts_number(self):
        self.hosts_number = pow(2, (32 - self.nbits)) - 2
        pass

    def calculate_subnets_number(self):
        octetCount = 0
        for x in self.subnet_mask:
            if x == 255:
                octetCount = octetCount + 1
        octetCount = octetCount * 8
        self.subnet_number = pow(2, self.nbits - octetCount)
        pass

    def negate_broadcast_address(self):
        broatcast = []
        for octet in self.subnet_mask:
            negate_octet = (1 << 8) - 1 - octet
            broatcast.append(negate_octet)

        return broatcast

    def generate_info(self):
        data = {}
        broadcast_addresses = []
        broadcast_negated = self.negate_broadcast_address()
        data["subnet"] = []
        for i in range(self.subnet_number):
            if i == 0:
                ip_address = self.ip_address
            else:
                ip_address = increment_address(broadcast_addresses[i - 1])
            broadcast_address = []
            for j in range(len(ip_address)):
                broadcast_address.append(ip_address[j] + broadcast_negated[j])
            broadcast_addresses.append(broadcast_address)
            firstHost = increment_address(ip_address)
            lastHost = decrement_address(broadcast_address)

            data["subnet"].append({
                'id': i+1,
                'ip_address': '.'.join(str(x) for x in ip_address),
                'ip_class': self.network_class,
                'subnet_mask': '.'.join(str(x) for x in self.subnet_mask),
                'subnet_mask_binary': '.'.join(to_binary(self.subnet_mask)),
                'broadcast_address': '.'.join(str(x) for x in broadcast_address),
                'broadcast_address_binary': '.'.join(to_binary(broadcast_address)),
                'hosts': self.hosts_number,
                'hosts_binary': format(self.hosts_number, '08b'),
                'first_host_address': '.'.join(str(x) for x in firstHost),
                'first_host_address_binary': '.'.join(to_binary(firstHost)),
                'last_host_address': '.'.join(str(x) for x in lastHost),
                'last_host_address_binary': '.'.join(to_binary(lastHost))
            })
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)

            print "Podsiec {0}".format(i + 1)
            print "Adres podsieci {0}".format('.'.join(str(x) for x in ip_address))
            print "Klasa {0}".format(self.network_class)
            print "Maska podsieci {0}".format('.'.join(str(x) for x in self.subnet_mask))
            print "Maska podsieci binarnie {0}".format('.'.join(to_binary(self.subnet_mask)))
            print "Adres rozgloszeniowy {0}".format('.'.join(str(x) for x in broadcast_address))
            print "Adres rozgloszeniowy binarnie {0}".format('.'.join(to_binary(broadcast_address)))
            print "Liczba hostow {0}".format(self.hosts_number)
            print "Liczba hostow binarnie {:010b}".format(self.hosts_number)
            print "Adres pierwszego hosta {0}".format('.'.join(str(x) for x in firstHost))
            print "Adres pierwszego hosta binarnie {0}".format('.'.join(to_binary(firstHost)))
            print "Adres ostatniego hosta {0}".format('.'.join(str(x) for x in lastHost))
            print "Adres ostatniego hosta binarnie {0}".format('.'.join(to_binary(lastHost)))

            print '\n'
        pass
