#! /bin/python3

"""
Script by Ramon Rivera

"""

from jnpr.junos import Device
from jnpr.junos.utils.sw import SW
from pprint import pprint

pkg = '/home/rrivera/scripts/junos_scripts/software_update/EX4200/jinstall-ex-4200-15.1R6-S2.1-domestic-signed.tgz'
with Device('10.254.11.13', user='admin', password='3p1c.2010k', port=22) as dev:

    sw = SW(dev)
    ok = sw.install(package=pkg, progress=True)
    if ok:
        sw.reboot()
    


