#! /bin/python3

"""
Script by Ramon Rivera

"""

from jnpr.junos import Device
from jnpr.junos.utils.sw import SW

pkg = '/home/rrivera/Downloads/jinstall-ex-4500-15.1R6-S2.1-domestic-signed.tgz'
with Device('10.255.6.166', user='root', password='wnt2770210', port=22) as dev:

    sw = SW(dev)
    ok = sw.install(package=pkg, progress=True)
    if ok:
        sw.reboot()
    


