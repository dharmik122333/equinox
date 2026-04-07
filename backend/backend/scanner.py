from scapy.all import ARP, Ether, srp
import socket

def scan_network():
    devices = []

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("Your IP:", local_ip)

    # Automatically detect subnet
    subnet = ".".join(local_ip.split(".")[:-1]) + ".1/24"

    print("Scanning network...\n")

    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=False)[0]

    for sent, received in result:
        print(f"IP: {received.psrc}  |  MAC: {received.hwsrc}")
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices