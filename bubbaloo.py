#!/usr/bin/python

import sys
import string
import GeoIP
import pytorctl.TorCtl as torctl
from time import sleep
import subprocess, shlex


CHECK_LOC_URL="http://stanford.edu/~yiannisy/cgi-bin/check_loc"
GOOGLE_BP_QUERY="http://google.com/search?q=pizza+delivery"
GOOGLE_BP_FETCH_OPTIONS="-U \"Firefox/3.0.15\""

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
            relays.append(relay)
    return relays

def get_countries(relays):
    countries = []
    for relay in relays:
        if relay['country'] not in countries:
            countries.append(relay['country'])
    return sorted(countries)
    

def list_relay(relay):
    print "%s\t%s\t%s" % (relay['name'],relay['ip'],relay['country'])

def list_relays(relays):
    for relay in relays:
        list_relay(relay)

def tor_connect():
    conn = torctl.connect(passphrase="test")
    return conn

def test_url(url, country, tor_conn, fetch_options=''):
    cmd = "wget -t 1 -T 10 --execute=http_proxy=127.0.0.1:8123 %s %s -O %s.html" % (url,fetch_options, country)
    args = shlex.split(cmd)
    _country_str = "{%s}" % country
    tor_conn.set_option("ExitNodes", _country_str)
    # wait to setup circuit for this country
    print "Fetching from %s" % country
    sleep(15)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = p.communicate()
            
def test_url_by_countries(url, relays, tor_conn, fetch_options=''):
    countries = get_countries(relays)
    for country in countries:
        if country:
#            country_relays = [ r for r in relays if r['country'] == country ]
            test_url(url, country, tor_conn, fetch_options)

if __name__ == "__main__":
    gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    relays = parse_consensus()
    tor_conn = tor_connect()
#   test_url(CHECK_LOC_URL, "US", tor_conn)
#    test_url(CHECK_LOC_URL, "GR", tor_conn)
#    test_url_by_countries(CHECK_LOC_URL, relays, tor_conn)
    test_url_by_countries(GOOGLE_BP_QUERY, relays, tor_conn, GOOGLE_BP_FETCH_OPTIONS,)
#    list_relays(relays)
#    test_bp(relays)
