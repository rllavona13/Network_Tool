import sys
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen

if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " host community maxRepititions")
    exit(1)

host = sys.argv[1]
community = sys.argv[2]
maxRepeatitions = int(sys.argv[3])
nonRepeaters 	= 0

errIndication, errStatus, errIndex, varBinds = cmdgen.CommandGenerator().bulkCmd(cmdgen.CommunityData(community),
    cmdgen.UdpTransportTarget((host, 161)),
    nonRepeaters, maxRepeatitions,
    cmdgen.MibVariable('IF-MIB', 'ifDescr'))

i = 0
for varBind in varBinds:
    i += 1
    for oid, val in varBind:
        print("Interface: " + str(i) + " oid: " + str(oid) + ", val: " + str(val))
