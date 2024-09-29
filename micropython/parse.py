import struct

# Dictionaries for known vendor and product IDs
VENDOR_ID = {
    0x02E1: "VICTRON_ENERGY_BV",
}

PRODUCT_ID = {
    0xA054: "SMARTSOLAR_MPPT_75_10",
}

def parse_ble_adv_data(ble_adv_data):
    # Define the BLE advertisement header format: 'BBBBBBB18s' (5 bytes, 2 bytes for vendor, and 18 bytes for manufacturer-specific data)
    ble_header_format = 'BBBBBBB18s'

    # Unpack the BLE advertisement header
    ble_header_data = struct.unpack(ble_header_format, ble_adv_data)

    # Extract meaningful fields
    flags, length, data_type, man_data_len, man_data_type, vendor1, vendor2, manufacturer_data = ble_header_data

    # Combine the two vendor bytes into a byte sequence
    vendor_bytes = bytes([vendor1, vendor2])

    # Unpack the combined vendor bytes as a 16-bit little-endian value
    vendor_id = struct.unpack('<H', vendor_bytes)[0]  # Use little-endian for Vendor ID
    vendor_name = VENDOR_ID.get(vendor_id, f"Unknown Vendor (0x{vendor_id:04X})")

    # Define the format of the manufacturer-specific data
    manufacturer_specific_format = 'BBHBBBB10s'

    # Unpack the manufacturer-specific data
    unpacked_manufacturer_data = struct.unpack(manufacturer_specific_format, manufacturer_data)

    # Extract fields from the manufacturer-specific data
    man_prod_adv, man_rec_len, man_prod_id, man_rec_type, man_counter_lsb, man_counter_msb, man_encryption_key_byte_0, man_encrypted_data = unpacked_manufacturer_data
    product_name = PRODUCT_ID.get(man_prod_id, f"Unknown Product (0x{man_prod_id:04X})")

    # Build the dictionary with all relevant data
    result = {
        "vendor_id": vendor_name,
        "product_advertisement": f"0x{man_prod_adv:02X}",
        "record_length": man_rec_len,
        "product_id": product_name,
        "record_type": man_rec_type,
        "counter_lsb": man_counter_lsb,
        "counter_msb": man_counter_msb,
        "encryption_key_byte_0": f"0x{man_encryption_key_byte_0:02X}",
        "encrypted_data": man_encrypted_data,
    }

    return result


def main():
    # Example usage
    ble_adv_data = b'xxx'
    parsed_data = parse_ble_adv_data(ble_adv_data)

    # Print the parsed dictionary
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()

