import pytest

from command_parser import parse_cmd_top, parse_cmd_ip, process_ip_list

top = [
    ("10", "root", "0,3", "0,0", "rcu_sched"),
    ("877", "root", "6,6", "0,8", "Xorg"),
    ("1209", "george", "0,3", "0,1", "kded5"),
    ("1258", "george", "0,3", "0,2", "kactivitymanage"),
    ("1266", "george", "6,3", "0,8", "kwin_x11"),
    ("1270", "george", "2,0", "3,0", "plasmashell"),
    ("1349", "george", "5,0", "5,0", "thunderbird"),
    ("1379", "george", "0,3", "0,0", "dbus-daemon"),
    ("1633", "george", "1,3", "10,1", "chrome"),
    ("1680", "george", "0,3", "2,0", "chrome"),
    ("1746", "george", "0,3", "0,0", "at-spi2-registr"),
    ("315498", "george", "2,0", "10,0", "chrome"),
    ("321995", "george", "0,3", "2,2", "chrome"),
    ("328718", "george", "6,3", "1,7", "konsole"),
    ("328731", "george", "0,7", "0,1", "top"),
]

ip_list = [
    {
        'name': 'lo', 
        'flags': ['LOOPBACK', 'UP', 'LOWER_UP'], 
        'mac': '00:00:00:00:00:00', 
        'inet': '127.0.0.1/8', 
        'inet6': '::1/128'
    }, 
    {
        'name': 'eno1', 
        'flags': ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP'], 
        'mac': '2c:24:a7:49:99:e6', 
        'inet': '192.168.0.142/24', 
        'inet6': 'fe80::7daab:5fb6:efa9:2bca/64'
    }, 
    {
        'name': '8ee654dfa368e8', 
        'flags': ['NO-CARRIER', 'BROADCAST', 'MULTICAST', 'UP'], 
        'mac': '02:42:49:b5:df:b2', 
        'inet': '173.29.0.1/16', 
    }, 
    {
        'name': 'docker0', 
        'flags': ['NO-CARRIER', 'BROADCAST', 'MULTICAST', 'UP'], 
        'mac': '02:82:c5:9f:12:04', 
        'inet': '176.15.0.1/16', 
    },
    {
        'name': 'llw0', 
        'flags': ['UP', 'BROADCAST', 'SMART', 'RUNNING', 'SIMPLEX', 'MULTICAST'], 
        'mac': '46:3f:9d:48:78:2d', 
        'inet6': 'fb81::645e:2d3f:fe37:780d/64',
    }
]

all_list = {'inet': ['8ee654dfa368e8', 'docker0'], 
            'inet6': ['llw0'], 
            'both': ['lo', 'eno1']}

no_carrier_list = {'inet': ['8ee654dfa368e8', 'docker0'], 
                   'inet6': [], 
                   'both': []}

multicast_list = {'inet': ['8ee654dfa368e8', 'docker0'],
                  'inet6': ['llw0'], 
                  'both': ['eno1']}


def test_parse_cmd_top():
    output = parse_cmd_top("top.txt")
    assert top == output


def test_parse_cmd_ip():
    output = parse_cmd_ip("ip.txt")
    assert ip_list == output


def test_process_ip_list():
    ip_output = parse_cmd_ip("ip.txt")

    process_ip_output = process_ip_list(ip_output)
    process_no_carrier_output = process_ip_list(ip_output, flag="NO-CARRIER")
    process_multicast_output = process_ip_list(ip_output, flag="MULTICAST")

    assert process_ip_output == all_list
    assert process_no_carrier_output == no_carrier_list
    assert process_multicast_output == process_multicast_output
