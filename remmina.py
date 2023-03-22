#!/bin/python3
file = "inventories/test01/inventory"
with open(file, 'r') as inventory:
    lines = inventory.readlines()
    print('hosts:')
    for line in lines:
        t = line.split()
        if len(t) > 1:
            ip = t[1].split('=')[1]
            string_ip = ip.replace('.', '_')
           # name = t[2].split('=')[1]
            print(f'  - host_name: {t[0]}')
            print(f'    host_ip: {ip}')
            print(f'    string_ip: {string_ip}')
            print(f'    group: test01')
