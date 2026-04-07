vendors = {
    "6C:F6:DA": "Dell Laptop",
    "DE:F9:AF": "Mobile Device",
    "F2:D2:28": "Android Device",
    "68:39:43": "IoT Device",
}

def get_vendor(mac):
    prefix = mac.upper()[0:8]
    return vendors.get(prefix, "Unknown Device")