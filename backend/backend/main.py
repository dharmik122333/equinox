from scanner import scan_network
from monitor import start_monitoring

print("Scanning devices...\n")
devices = scan_network()

print("\nConnected Devices:")
for device in devices:
    print(f"IP: {device['ip']} | MAC: {device['mac']}")

print("\nStarting Traffic Monitoring...\n")

start_monitoring()
