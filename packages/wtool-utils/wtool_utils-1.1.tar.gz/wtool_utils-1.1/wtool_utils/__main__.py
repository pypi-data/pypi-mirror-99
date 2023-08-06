from argparse import ArgumentParser
from os import geteuid

from wtool_utils import *


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--interfaces", help="Return NIC information", action="store_true")
    ap.add_argument("-s", "--sniff", help="Sniff on interface. -i required", action="store_true")
    ap.add_argument("-if", "--interface", help="Specify NIC for -i & -s", type=str)
    ap.add_argument("-sf", "--sniff-filters", help="Specify BPF filters for the sniffer", type=str, default="")
    ap.add_argument("-sc", "--sniff-count", help="Only capture this amount of packets", type=int, default=-1)
    ap.add_argument("-sp", "--sniff-promisc", help="Enable promiscuous mode for sniffer", action="store_true")
    ap.add_argument("-so", "--sniff-output", help="Also write sniffed data to specified file", type=str, default=None)
    ap.add_argument("--self-test", help="Execute a self test and output the results.", action="store_true")
    a = ap.parse_args()

    if a.interfaces:
        data = {}
        if a.interface:
            data["interfaces"] = [get_addresses(a.interface)]
        else:
            data["interfaces"] = get_all_addresses()
        print(dumps(data))

    elif a.sniff:
        if not a.interface:
            print(dumps({"error": "no_iface"}))
            exit()
        else:
            if geteuid() != 0:
                print(dumps({"error": "no_root"}))
            else:
                sniff(a.interface, a.sniff_filters, a.sniff_count, a.sniff_promisc, a.sniff_output)

    elif a.self_test:
        data = {
            "interface_lookup": len(get_interfaces()) > 0,
            "interface_info": get_addresses(get_interfaces()[0]) is not None,
            "sniffing": True,  # TODO
        }
        print(dumps(data))


if __name__ == '__main__':
    main()
