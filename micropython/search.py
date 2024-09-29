import ubluetooth
import ubinascii
import struct
import time

from struct import unpack

from parse import parse_ble_adv_data
from decrypt import decrypt_message

# Define constants for BLE events
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

# Define the target MAC address in simplified format (no colons, e.g., 'e91234aaffee')
TARGET_MAC = 'e91234aaffee'.lower()

class BLEScanner:
    def __init__(self):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.scan_callback = None
        self.scanning = False  # Track the scanning state

    def ble_irq(self, event, data):
        # Check if it's a scan result
        if event == IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            # Convert the binary MAC address to a plain string without colons
            mac_address = ubinascii.hexlify(addr).decode('utf-8')

            # Check if the detected MAC matches the target MAC in plain format
            if mac_address.lower() == TARGET_MAC:
                #print(f"Target device found! MAC: {mac_address}, RSSI: {rssi}")
                #print(f"Advertisement data: {ubinascii.hexlify(adv_data)}")
                parsed_adv_data = self.parse_adv_data(adv_data)  # Parse the adv_data

                if self.scan_callback:
                    self.scan_callback(mac_address, rssi, parsed_adv_data)

        # Check if the scan is complete
        elif event == IRQ_SCAN_DONE:
            print("Scan completed.")
            self.stop_scan()

    def parse_adv_data(self, adv_data):
        """Parse the advertisement data from BLE broadcast packets"""
        parsed_adv_data = parse_ble_adv_data(bytes(adv_data))
        return parsed_adv_data
        

    def start_scan(self, duration=5000, callback=None):
        """Start scanning for BLE devices"""
        self.scan_callback = callback
        self.scanning = True
        self.ble.gap_scan(duration, 30000, 30000)
        print("Scanning started...")

    def stop_scan(self):
        """Stop scanning and deactivate BLE"""
        if self.scanning:
            self.ble.gap_scan(None)  # Stop scanning
            self.scanning = False
            print("Scanning stopped.")
        self.ble.active(False)  # Disable BLE

# Usage example
def device_found_callback(mac, rssi, parsed_adv_data):
    #print(f"Device with MAC {mac} found, RSSI: {rssi}")
    print(f"Raw Advertisement Data: {parsed_adv_data}")

# Initialize scanner
scanner = BLEScanner()
scanner.start_scan(duration=1000, callback=device_found_callback)

# Allow some time for the scan to complete
time.sleep(2)

# Ensure the scan is stopped gracefully if not already stopped
scanner.stop_scan()


