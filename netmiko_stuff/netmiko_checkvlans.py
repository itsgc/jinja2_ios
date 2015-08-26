#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import paramiko
import re
import operator
from netmiko import ConnectHandler

with open("device_settings.yml", 'r') as ymlfile:
    network_device = yaml.load(ymlfile)

net_connect = ConnectHandler(**network_device)
vlan_output = net_connect.send_command('show vlan brief')
active_vlans = dict()

def extract_vlans(input,exceptions=(1002,1003,1004,1005)):
	input = input.splitlines()
	input = input[3:]
	for line in input:
		if re.match(r'\S', line):
			vlan = line.split()
			vlan_id = int(vlan[0])
			vlan_name = str(vlan[1])
		if vlan_id not in exceptions:
			active_vlans.update({vlan_id:vlan_name})
	return active_vlans
output = extract_vlans(vlan_output)
print 'Active VLANs'
print '{0:10} {1:20}'.format("VLAN ID", "VLAN NAME")
for keys, values in sorted(output.iteritems(), key=operator.itemgetter(0)):
	print '{0:10} {1:20}'.format(keys,values)
