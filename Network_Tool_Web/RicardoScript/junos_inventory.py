#!/usr/bin/python
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import pandas as pd
import os

# Handle the JSON file to use in the host list.
config_file = open('ip_list.json')
ip_list = json.load(config_file)
config_file.close()

#csv_file = open('juniper_inventory.csv', 'r+b')

junos_identity = 'iso.3.6.1.2.1.1.5.0'
junos_serial_number = 'iso.3.6.1.4.1.2636.3.1.3.0'
junos_type = 'iso.3.6.1.4.1.2636.3.1.2.0'  # Device type, EX, MX, M10 etc...


def get_junos_identity(device_ip):  # pretty much explained.
    snmp_gen = cmdgen.CommandGenerator()
    try:
        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('c4ct1!'),
            cmdgen.UdpTransportTarget((device_ip, 161)), junos_identity)
        for name, val in varbinds:
            juniper_identity = str(val)
            # print('Item NAME Added')
            return juniper_identity
    except Exception as error:
        print(error)


def get_junos_serial(device_ip):  # pretty much explained
    snmp_gen = cmdgen.CommandGenerator()
    try:
        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('c4ct1!'),
            cmdgen.UdpTransportTarget((device_ip, 161)), junos_serial_number)
        for name, val in varbinds:
            juniper_serial = str(val)
            # print('Item SERIAL NAME Added')
            return juniper_serial
    except Exception as error:
        print(error)


def get_junos_type(device_ip):  # pretty much explained as well.
    snmp_gen = cmdgen.CommandGenerator()
    try:
        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('c4ct1!'),
            cmdgen.UdpTransportTarget((device_ip, 161)), junos_type)
        for name, val in varbinds:
            juniper_type = str(val)
            # print('Item DEVICE MODEL Added')
            return juniper_type
    except Exception as ex:
        print(ex)


def save_output(device_ip):  # function to save output into a CSV
    csv_file= 'juniper_inventory.csv'
    name = get_junos_identity(device_ip)
    serial = get_junos_serial(device_ip)
    device_type = get_junos_type(device_ip)
    snmp_objects_list = [device_ip, name, serial, device_type]
    col_titles = ('IP Address', 'Juniper Identity',  'Juniper Serial Number', 'Device Model')
    data = pd.np.array(snmp_objects_list).reshape((len(snmp_objects_list) // 4, 4))
    if not os.path.isfile(csv_file):
        pd.DataFrame(data, columns=col_titles).to_csv(csv_file,mode='w',index=False)
    else:
        pd.DataFrame(data).to_csv(csv_file,mode='a',index=False,header=False)


for i in ip_list['ip']:
    save_output(i)
    print('Adding %s done.' % i)
