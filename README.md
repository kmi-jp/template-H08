# H08: Command Parser
Vytvořte modul `command_parser.py` obsahující funkce `parse_cmd_top(path)`, `parse_cmd_ip(path)` a `process_ip_list(ip_list, flag=None)`. První dvě funkce pracují se soubory `top.txt` a `ip.txt`, které obsahují výstupy příkazů `top` a `ip a` (oba výstupy jsou z linuxové distribuce Kubuntu).

**Snažte se nejvíce využít regulární výrazy.**

## parse_cmd_top

Tato funkce ze souboru načte informace o běžících procesech (výstup příkazu `top`) a do seznamu uloží pro každý proces tuple ve tvaru: (PID, USER, %CPU, %MEM, COMMAND). Záznamy v seznamu budou seřazeny vzestupně podle PID. 


Kód bude testován oproti souboru `top.txt` (jednotlivé hodnoty v sloupcích jsou odděleny whitespace znaky).
```
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND               
    877 root      20   0  437440  31476  17524 S   6,6   0,8 281:13.71 Xorg   
   1266 george    20   0 2916944  31592  20012 S   6,3   0,8 349:07.69 kwin_x11              
```

Příklad výstupu:

```python
from command_parser import parse_cmd_top

top_list = [
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

output = parse_cmd_top("top.txt")
assert top_list == output
```

## parse_cmd_ip

Tato funkce ze souboru načte informace o síťových rozhraních (výstup příkazu `ip a`) a do seznamu uloží pro každé rozhraní slovník obsahující informace o jeho příznacích, mac a ip adresách.

Například pro rozhraní (2. v pořadí ve výpisu, viz. soubor `ip.txt`):
```
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 2c:24:a7:49:99:e6 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.142/24 brd 192.168.0.255 scope global dynamic noprefixroute eno1
       valid_lft 7195sec preferred_lft 7195sec
    inet6 fe80::7daab:5fb6:efa9:2bca/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```
Vytvoří následující slovník:
```python
{
    'name': 'eno1', 
    'flags': ['BROADCAST', 'MULTICAST', 'UP', 'LOWER_UP'], 
    'mac': '2c:24:a7:49:99:e6', 
    'inet': '192.168.0.142/24', 
    'inet6': 'fe80::7daab:5fb6:efa9:2bca/64'
}
```

Příklad celého výstupu:
```python
from command_parser import parse_cmd_ip

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
        'inet6': 'fe80::7dab:5fb6:efa9:2bca/64'
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
        'inet6': 'fb81::645e:2d3f:fe37:780d/64'
    }
]

ip_output = parse_cmd_ip("ip.txt")
assert ip_list == ip_output
```

## process_ip_list

Funkce `proces_list(ip_list, flag=None)` bere jako vstup seznam, který je výstupem funkce `parse_cmd_ip` a roztřídí podle ip adres jména jednotlivých síťových rozhraní do tří kategorií (`inet`, `inet6` a `both`, podle toho jake adresy má rozhraní k dispozici). Výsledkem pak bude slovník, který pro tyto tři kategorie obsahuje seznam jmen rozhraní. Pokud je navíc zadán nepovinný parametr `flag`, výsledek obsahuje pouze rozhraní, které mají daný příznak.

**Pro zpracování parametru `ip_list` použijte strukturální rozpoznávání vzorů.**

Příklad výstupu:
```python
from command_parser import process_ip_list, parse_cmd_ip

all_list = {'inet': ['8ee654dfa368e8', 'docker0'], 
            'inet6': ['llw0'], 
            'both': ['lo', 'eno1']}

no_carrier_list = {'inet': ['8ee654dfa368e8', 'docker0'], 
                   'inet6': [], 
                   'both': []}

multicast_list = {'inet': ['8ee654dfa368e8', 'docker0'],
                  'inet6': ['llw0'], 
                  'both': ['eno1']}

ip_output = parse_cmd_ip("ip.txt")
process_ip_output = process_ip_list(ip_output)
process_no_carrier_output = process_ip_list(ip_output, flag="NO-CARRIER")
process_multicast_output = process_ip_list(ip_output, flag="MULTICAST")

assert process_ip_output == all_list
assert process_no_carrier_output == no_carrier_list
assert process_multicast_output == process_multicast_output
```

## Lokální testování
Funkčnost řešení ověříte následujícím příkazem:

```bash
pytest tests.py
```
