#!/usr/bin/env python3
# Version: v1.0.0 @2023

###########################################
#    Author: Mirabbas Aghalarov           #
#    Youtube: mirabbasaghalarov           #
#    Instagram: 1mirabbas                 #
#    Linkedin: mirabbasagalarov           #
#    Email: mirabbasagalarov0@gmail.com   #
###########################################

import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", help="target domain", dest='domain')
parser.add_argument("-o", help="output file", dest='output')

args = parser.parse_args()
domain = args.domain
output = args.output

def prRed(skk):print("\033[91m{}\033[00m".format(skk))
def prCyan(skk):print("\033[96m{}\033[00m".format(skk))
def prGreen(skk):print("\033[92m{}\033[00m".format(skk))
def prMagenta(skk):print("\033[35m{}\033[00m".format(skk))

lists=[]

prCyan('''
  ____      _                _     
 / ___|_ __| |_ ___ _ __ ___| |__  
| |   | '__| __/ __| '__/ __| '_ \ 
| |___| |  | |_\__ \ | | (__| | | |
 \____|_|   \__|___/_|  \___|_| |_|
       Author: Mirabbas Aghalarov                           

''')
prGreen('''
1)Default result
2)Domain
''')
try:
    value = input('Please select the mode: ')
    value=int(value)
except ValueError:
    prRed('Error')


if domain is None:
    prRed("""Missing target! ==>","Usage: crtsrch.py -d target.com""")
    print("")
else:
    if output is None:
        if value == 1:
            response = requests.get('https://crt.sh/?q=' + domain + '&output=json')
            json = response.json()
            for i in json:
                print(i['common_name'])
        elif value ==2:
            response = requests.get('https://crt.sh/?q=' + domain + '&output=json')
            json = response.json()
            for i in json:
                a=i['common_name']
                a=str(a)
                print(a.replace('*.', ''))
        else:
            prRed('''Please choose the mode properly''')
    else:
        with open(output, "a") as f:
            if value == 1:
                response = requests.get('https://crt.sh/?q=' + domain + '&output=json')
                json = response.json()
                for i in json:
                    c=i['common_name']
                    c=str(c)
                    f.write(c+'\n')
            elif value ==2:
                response = requests.get('https://crt.sh/?q=' + domain + '&output=json')
                json = response.json()
                for i in json:
                    d=i['common_name']
                    d=str(d)
                    m=d.replace('*.', '')
                    f.write(m+'\n')
