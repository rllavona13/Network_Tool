"""
Script to upgrade Juniper devices
Script By Ramon Rivera

"""

from jnpr.junos import Device
from jnpr.junos.utils.sw import SW


def upgrader():
    pkg = 'SRX210/junos-srxsme-12.1X46-D72.2-domestic.tgz'
    with Device(host='10.0.1.2', user='admin', password='3p1c.2010k', port=22) as dev:

        sw = SW(dev)
        ok = sw.install(package=pkg, progress=True)
        if ok:
            sw.reboot()


if __name__ == '__main__':
    upgrader()

