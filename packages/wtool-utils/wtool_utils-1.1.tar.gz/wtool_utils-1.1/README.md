# wtool utils
## features
- [X] get nic information
- [X] sniffing on interface
    - [ ] interpreting / dissecting packets

## installation
```shell
sudo pip3 install wtool_utils
# or 
sudo pip3 install git+https://github.com/nbdy/wtool_utils
# or
cd /tmp/ ; git clone https://github.com/nbdy/wtool_utils ; cd wtool_utils
sudo pip3 install .
```
## usage
```shell
$wtool_utils --help
usage: wtool_utils [-h] [-i] [-s] [-if INTERFACE] [-sf SNIFF_FILTERS] [-sc SNIFF_COUNT] [-sp] [-so SNIFF_OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interfaces      Return NIC information
  -s, --sniff           Sniff on interface. -i required
  -if INTERFACE, --interface INTERFACE
                        Specify NIC for -i & -s
  -sf SNIFF_FILTERS, --sniff-filters SNIFF_FILTERS
                        Specify BPF filters for the sniffer
  -sc SNIFF_COUNT, --sniff-count SNIFF_COUNT
                        Only capture this amount of packets
  -sp, --sniff-promisc  Enable promiscuous mode for sniffer
  -so SNIFF_OUTPUT, --sniff-output SNIFF_OUTPUT
                        Also write sniffed data to specified file
```