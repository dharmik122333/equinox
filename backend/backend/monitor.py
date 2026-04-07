from scapy.all import sniff
from collections import defaultdict
import time
from logger import log_alert
from vendor import get_vendor
import socket

traffic = defaultdict(int)
mac_map = {}
known_devices = set()
previous_traffic = {}
blocked_devices = set()

# ⭐ Shared data for web dashboard
shared_data = {}

start_time = time.time()

local_ip = socket.gethostbyname(socket.gethostname())

def process_packet(packet):
    global traffic, mac_map, start_time, known_devices, previous_traffic, blocked_devices, shared_data

    if packet.haslayer("Ether") and packet.haslayer("IP"):
        src_ip = packet["IP"].src
        src_mac = packet["Ether"].src

        if src_ip in blocked_devices:
            return

        traffic[src_ip] += 1
        mac_map[src_ip] = src_mac

        if (
            src_ip.startswith("192.168.")
            and src_ip not in known_devices
            and src_ip != local_ip
        ):
            print(f"⚠ NEW DEVICE DETECTED: {src_ip}")
            log_alert(f"New device detected: {src_ip}")
            known_devices.add(src_ip)

    current_time = time.time()
    elapsed = current_time - start_time

    if elapsed >= 5:

        print("\n📊 Local Device Traffic Report:")

        local_traffic = {
            ip: count for ip, count in traffic.items()
            if ip.startswith("192.168.")
        }

        if local_traffic:
            # ⭐ Share data to dashboard
            shared_data.clear()
            shared_data.update(local_traffic)

            sorted_devices = sorted(local_traffic.items(), key=lambda x: x[1], reverse=True)

            for ip, count in sorted_devices:
                mac = mac_map.get(ip, "Unknown")
                vendor = get_vendor(mac)

                if count < 200:
                    level = "LOW"
                elif count < 500:
                    level = "MEDIUM"
                else:
                    level = "HIGH"

                print(f"{ip} | {vendor} | {count} packets | {level}")

            top_ip = sorted_devices[0][0]
            top_count = sorted_devices[0][1]

            print(f"\n🏆 Top Talker: {top_ip}")

            if top_count > 500:
                print("🚨 UNDER THREAT")
            else:
                print("✅ SECURE")

            # 🔥 Logging alerts
            if top_count > 700:
                log_alert(f"High traffic from {top_ip}")
                blocked_devices.add(top_ip)

        traffic.clear()
        start_time = time.time()

def start_monitoring():
    print("Monitoring network traffic...\n")
    sniff(prn=process_packet, store=False)