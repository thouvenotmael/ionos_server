#!/bin/bash

# Afficher les connexions des utilisateurs durant les 24 dernières heures
echo "# Utilisateurs connectés durant les 24 dernières heures :"
Day=$(date --date='24 hours ago' '+%d-%m-%Y');day=$(date --date='24 hours ago' '+%a %b %d'); last -i| grep -e"$day" | awk -v day=$Day '{print "connection_system;"day";"$3}'
echo "# Adresses bannies Fail2ban"
Day=$(date --date='24 hours ago' '+%d-%m-%Y');day=$(date --date='24 hours ago' '+%Y-%m-%d'); cat /var/log/fail2ban.log | grep -E "^$day" | grep -e "NOTICE  \[sshd\] Ban" | awk -v day=$Day '{for(i=1;i<=NF;i++) if($i ~ /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/) print "address_ban_fail2ban;"day";"$i}'
echo "# Adresses identifiées sur serveur web"
day=$(date --date='24 hours ago' '+%d-%m-%Y'); cat /home/appli/log/logfile.log | grep $day | awk '{ print "address_identify_web_server;"$1";"$2}' 
