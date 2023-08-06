from netifaces import interfaces, ifaddresses
from pylibpcap.base import Sniff
from bson import dumps


def check_iface(iface):
    return iface is not None and iface in interfaces()


def get_interfaces():
    return interfaces()


def get_addresses(iface):
    if not check_iface(iface):
        return {}
    return {iface: ifaddresses(iface)}


def get_all_addresses():
    r = []
    for iface in get_interfaces():
        r.append(get_addresses(iface))
    return r


def sniff(iface, filters="", count=-1, promisc=0, out_file=None):
    if not check_iface(iface):
        return {}
    sniffer = Sniff(iface, filters=filters, count=count, promisc=promisc, out_file=out_file)
    for plen, t, buf in sniffer.capture():
        stats = sniffer.stats()
        print(dumps({
            "length": plen,
            "time": t,
            "payload": buf,
            "cap_cnt": stats.capture_cnt,
            "recv_cnt": stats.ps_recv,
            "drop_cnt": stats.ps_drop,
            "ifdrop_cnt": stats.ps_ifdrop
        }))


__all__ = ['get_interfaces', 'get_addresses', 'get_all_addresses', 'dumps', 'sniff']
