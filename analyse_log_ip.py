#!/usr/bin/python3

"""
Description: Analyse le fichier de log des adresses ip obtenu par le script bash daily_check.sh
             , il est du type :
                type_alerte;date;@_IP
                Le type alerte prend les valeurs : address_identify_web_server, connection_system, address_ban_fail2ban
                exemple fichier : log/daily_check.log
                # Utilisateurs connectés durant les 24 dernières heures :
                connection_system;27-02-2025;86.253.56.157
                connection_system;27-02-2025;86.253.56.157
                connection_system;27-02-2025;86.253.56.157
                # Adresses bannies Fail2ban
                address_ban_fail2ban;27-02-2025;116.110.116.182
Version 1.0 by Maël Thouvenot
Initial version
"""
import argparse
import sys
import requests
import json
import time
import ipaddress
import os
import csv
import re
from datetime import datetime, timedelta
import logging
import requests

log = logging.getLogger(__name__)   
Path_log = '/home/appli/'
Logfile_name = 'Debug_Analyse_log_ip'

def find_ipv4_address(text):
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return None

def key_pressed():
    keypressed=''

    while ((keypressed !='y' )):
          keypressed = str(input("Appuyez sur 'y' pour continuer "))

def parseArgs():
    '''
    Parse the command line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.description = 'Analyse logfile du script daily_check.sh '
    parser.add_argument('--debug', help='Debug provides some additional info',
                        dest='debug', action='store_true')
    parser.add_argument('--file', help='file logfile',
                        dest='filename', action='store')
    parser.set_defaults(filename="")
    parser.set_defaults(debug=False)
    return parser.parse_args()

if __name__ == "__main__":
    # Get the command line arguments and checks
    args = parseArgs()
    value_required_args=0
    # define a handler to write INFO messages or higher to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    log.setLevel(logging.INFO)
     # create a format to be used for console messages.
    formatter = logging.Formatter('%(message)s')
     # assign the formater to the console handler.
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    # set up the logging, we log to console and file.
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    #stream=sys.stdout,
                    filename=(f'{Logfile_name}.log'),
                    filemode='w')
    if args.debug:
       console.setLevel(logging.DEBUG)
       log.setLevel(logging.DEBUG)
    else:
       console.setLevel(logging.INFO)
       log.setLevel(logging.INFO)

    if (args.filename!=""):
        value_required_args = value_required_args+1

    if (value_required_args != 1):
        (argparse.ArgumentParser()).error("parameters --file filename mandatory")
        quit()
    if (args.filename!="") :
       InputFilename = args.filename
       log.info(f"Fichier d'entrée : {InputFilename}")
       if (os.path.isfile(InputFilename) == False) :
          log.info(f"Le fichier n'existe pas")
          quit()

    # Obtenir la date d'hier
    hier = datetime.now() - timedelta(days=1)

    # Formater la date
    date_hier = hier.strftime("%d-%m-%Y")
    log.info(f"date de hier : {date_hier}")
    inputfile = open(InputFilename, newline='\n')
    dict_adresse_ip = {}
    for line in inputfile:
        line = line.replace("\n","")
        if line.startswith("#") :
            continue
        elif line.split(";")[1]==date_hier :
             if line.split(";")[2] not in dict_adresse_ip.keys() :
                 dict_adresse_ip[line.split(";")[2]] = {}
                 dict_adresse_ip[line.split(";")[2]].update({line.split(";")[0]:1})
             elif line.split(";")[0] not in dict_adresse_ip[line.split(";")[2]].keys():
                 dict_adresse_ip[line.split(";")[2]].update({line.split(";")[0]:1}) 
             else :
                 iteration = dict_adresse_ip[line.split(";")[2]][line.split(";")[0]]+1
                 dict_adresse_ip[line.split(";")[2]][line.split(";")[0]] = iteration
        else :
            continue
    print(f"{dict_adresse_ip}")
    for address in dict_adresse_ip.keys():
        url = f"https://freeipapi.com/api/json/{address}"
        response = requests.get(url)
        data = response.json()
        print(f"{address} : {data['cityName']} - {data['countryName']} - {data['continent']} {dict_adresse_ip[address]}")

