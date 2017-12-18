#!/usr/bin/python
#
# read /var/run/hostapd for interfaces to poll
# read process list to find list of running hostapds (or get from hostapd_cli)
# get mac address, connected time, transmitted packets
# read arp table
# match arp address to ip address
# print matches
# rinse repeat

import os, re, sys, time, string
import subprocess, humanize as pp

from netaddr import *

hostapd_control_path = '/var/run/hostapd'
hostapd_cli_path = '/usr/sbin/hostapd_cli'

ifconfig_path = '/sbin/ifconfig'

arp_path = '/usr/sbin/arp'
arp_flags = '-an'

hostapd_interfaces = os.listdir(hostapd_control_path)
hostapd_uptime = 0

clients = dict()
arp_table = dict()
hostapd_stats = dict()

def get_hostapd():
  global hostapd_uptime
  for hostapd_iface in hostapd_interfaces:
    hostapd_cli_cmd = [hostapd_cli_path,'-i',hostapd_iface,'all_sta']
    hostapd_uptime = time.time() - int(os.stat('%s/%s' % (hostapd_control_path, hostapd_iface))[9])

    all_sta_output = subprocess.Popen(hostapd_cli_cmd,stdout=subprocess.PIPE).communicate()[0].decode()
    hostapd_output = subprocess.Popen([hostapd_cli_path,'status'], stdout=subprocess.PIPE)
    hostapd_output = hostapd_output.communicate()[0].decode().split('\n')

    channel = re.sub('channel=','', hostapd_output[16])
    bssid = re.sub('bssid\[0\]=','',hostapd_output[24])
    ssid = re.sub('ssid\[0\]=','',hostapd_output[25])
    clientcount = int(re.sub('num_sta\[0\]=','',hostapd_output[26]))

    hostapd_stats[hostapd_iface] = [ssid, bssid, channel, clientcount]

    macreg = r'^('+r'[:-]'.join([r'[0-9a-fA-F]{2}'] * 6)+r')$'
    stas = re.split(macreg, all_sta_output, flags=re.MULTILINE)

    mac = rx = tx = ctime = ''
    for sta_output in stas:

      for line in sta_output.split('\n'):
        if re.match(macreg,line):
          mac = line
        if re.match('rx_packets',line):
          rx = re.sub('rx_packets=','',line)
        if re.match('tx_packets',line):
          tx = re.sub('tx_packets=','',line)
        if re.match('connected_time=',line):
          ctime = re.sub('connected_time=','',line)

      if mac and rx and tx and ctime:
        clients[mac] = [ctime, rx, tx]

def get_arp_table():
  arp_output = subprocess.Popen([arp_path,arp_flags],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')

  for line in range(len(arp_output)):
    l = arp_output[line].split(' ')
    try:
      iface = l[6]

      if iface in hostapd_interfaces:
        ip = l[1]
        mac = l[3]

        if re.match('[A-Z0-9][A-Z0-9]:',mac,re.IGNORECASE):
          arp_table[mac] = [ip, iface]
    except:
      pass

def get_vendor(mac):
  try: vendor = EUI(mac).oui.registration().org
  except: vendor = 'Unknown'
  return vendor

get_hostapd()
get_arp_table()

for hostapd_iface in hostapd_interfaces:
  iface = hostapd_stats[hostapd_iface]
  print('%s (%s / %s, channel %s): %s Client%s, Started: %s' % ( iface[0], iface[1], get_vendor(iface[1]), iface[2],
      iface[3], 's' if iface[3]>1 else '',
      pp.naturaltime(hostapd_uptime) ))

  for mac in clients:
    print('  %s' % arp_table[mac][0])
    print('  [%s / %s]' % (mac, get_vendor(mac)))
    print(': connected %s, %sk in / %sk out' % (pp.naturaltime(clients[mac][2]), pp.intcomma(clients[mac][0]), pp.intcomma(clients[mac][1])))
