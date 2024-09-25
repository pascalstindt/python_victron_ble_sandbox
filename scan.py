import asyncio
from bleak import BleakScanner

VICTRON_PRODUCT_IDS = {
    0xA054: "SmartSolar MPPT 75|10",
}

MANUFACTURER_ID = 0x02E1  # Victron Manufacturer ID


def parse_device(device, advertisement_data):
    manu_data = advertisement_data.manufacturer_data.get(MANUFACTURER_ID)

    if manu_data and len(manu_data) >= 4:
        product_id = int.from_bytes(manu_data[2:4], "little")
        if product_id in VICTRON_PRODUCT_IDS:
            print(f"Found Victron device: {VICTRON_PRODUCT_IDS[product_id]} at {device.address}: {advertisement_data}")


async def scan():
    # Pass the callback directly to the BleakScanner constructor
    scanner = BleakScanner(detection_callback=parse_device)
    await scanner.start()
    await asyncio.sleep(10)  # Scanning for 10 seconds
    await scanner.stop()


if __name__ == "__main__":
    asyncio.run(scan())
