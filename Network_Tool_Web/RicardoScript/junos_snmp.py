from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import pandas as pd


# Handle the JSON file to use in the host list.
config_file = open('ip_list.json')
ip_list = json.load(config_file)
config_file.close()

csv_file = open('juniper_inventory.csv', 'r+b')

junos_identity = 'iso.3.6.1.2.1.1.5.0'  # Name of the juniper device
junos_serial_number = 'iso.3.6.1.4.1.2636.3.1.3.0'  # Serial number of the Juniper device
junos_type = 'iso.3.6.1.4.1.2636.3.1.2.0'  # Device type, EX, MX, M10 etc...


def get_junos_identity():  # pretty much explained.

    snmp_gen = cmdgen.CommandGenerator()

    try:
        for ip in ip_list['ip']:

            errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                cmdgen.CommunityData('c4ct1!'),
                cmdgen.UdpTransportTarget((ip, 161)), junos_identity)

            for name, val in varbinds:
                juniper_identity = str(val)

                return juniper_identity

    except Exception as ex:
        print(ex)


def get_junos_serial():  # pretty much explained

    snmp_gen = cmdgen.CommandGenerator()

    try:
        for ip in ip_list['ip']:

            errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                cmdgen.CommunityData('c4ct1!'),
                cmdgen.UdpTransportTarget((ip, 161)), junos_serial_number)

            for name, val in varbinds:
                juniper_serial = str(val)
                return juniper_serial

    except Exception as ex:
        print(ex)


def get_junos_type():  # pretty much explained as well.

    snmp_gen = cmdgen.CommandGenerator()

    try:
        for ip in ip_list['ip']:

            errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                cmdgen.CommunityData('c4ct1!'),
                cmdgen.UdpTransportTarget((ip, 161)), junos_type)

            for name, val in varbinds:
                juniper_type = str(val)
                return juniper_type

    except Exception as ex:
        print(ex)


def save_output():  # function to save output into a CSV

    name = get_junos_identity()
    serial = get_junos_serial()
    device_type = get_junos_type()

    mydevices = [name, serial, device_type]

    col_titles = ('Juniper Identity:',  'Juniper Serial Number:', 'Device Model:')
    data = pd.np.array(mydevices).reshape((len(mydevices) // 3, 3))
    pd.DataFrame(data, columns=col_titles).to_csv("juniper_inventory.csv", index=False)


#  Here i call the functions, i need to call one function and save that in the CSV in different rows
save_output()