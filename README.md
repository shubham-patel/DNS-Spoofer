# DNS Spoofer

A Python tool that intercepts DNS queries using netfilterqueue and redirects a target domain to a specified IP. When combined with ARP spoofing, it can redirect another device's web traffic to an attacker-controlled server.

> **Disclaimer:** For educational purposes and authorized testing only. Only use on networks you own or have explicit permission to test. Unauthorized use is illegal. The author is not responsible for any misuse.

---

## How it works

1. `iptables` routes packets through a local queue
2. netfilterqueue intercepts each DNS response packet
3. If the response matches the target domain, the resolved IP is replaced with the redirect IP
4. The modified packet is forwarded to the victim

## Requirements

```bash
pip install -r requirements.txt
```

> **Note:** Linux only. `netfilterqueue` does not work on macOS or Windows.

## Setup

Route traffic through the queue before running:

```bash
# To spoof for another device (run arp_spoofer first):
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0

# To spoof on your own machine:
sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
sudo iptables -I INPUT -j NFQUEUE --queue-num 0
```

## Usage

```bash
sudo python3 dns_spoofer.py -t <target_website> -r <redirect_ip>
```

```bash
sudo python3 dns_spoofer.py -t www.google.com -r 192.168.1.10
```

**After finishing, always reset iptables:**

```bash
sudo iptables --flush
```

---

## Part of [H-Tools](https://github.com/shubham-patel/H-Tools)

Built during B.Tech studies. H-Tools bundles this and other networking/security utilities in a single CLI menu.
