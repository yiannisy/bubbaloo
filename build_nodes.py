#!/usr/bin/python

import sys
import string
import GeoIP

## yiannis: The first number is the beginning of
## the IP address range; the second number is the
## end of the range. Both numbers are IP addresses,
## stored with the first dot-delimited piece of
## the address in the most significant byte

def parse_consensus():
    relays = []
    file = open('consensus.txt','r')
    lines = file.readlines()
    for line in lines:
        if string.find(line, 'r ') == 0:
            _relay = line.split(' ')
            name = _relay[1]
            fingerprint = _relay[2]
            ip = _relay[6]
            country =  gi.country_code_by_addr(ip)
            relay = { 'name':name, 'fingerprint':fingerprint, 'ip':ip, 'country':country }
            list_relay(relay)
            relays.append(relay)

def list_relay(relay):
    print "%s\t\t%s\t\t%s" % (relay['name'],relay['ip'],relay['country'])

def list_relays(relays):
    for relay in relays:
        list_relay(relay)
        
def test_bp(relays):
    pass
    

if __name__ == "__main__":
    gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    relays = parse_consensus()
    list_relays(relays)
    test_bp(relays)
