from construct import Struct, Int8ul, Enum, Int16ul, Bytes, GreedyBytes, BitsInteger, BitStruct
from Crypto.Cipher import AES
from Crypto.Util import Counter


def decrypt_message(key: hex, message: bytes, counter_lsb, counter_msb):
    # Convert the hex key to bytes
    key = bytes.fromhex(key)

    # Construct the nonce using data_counter_lsb and data_counter_msb
    nonce = bytes([counter_lsb, counter_msb] + [0] * 14)

    # Create a counter for CTR mode
    ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder="big"))

    # Create the AES cipher in CTR mode
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    # Decrypt the data
    decrypted_data = cipher.decrypt(message)

    return decrypted_data


raw_data = b"\x10\x02T\xa0\x01/0\xc0\xa1\xbab}+\xbb\x14\x00\xe9\xec\x08u"


ManufacturerData = Enum(
    Int8ul,
    Product_Advertisement=0x10,
)

ProductID = Enum(
    Int16ul,
    SmartSolar_MPPT_75_10=0xA054,
)

RecordType = Enum(
    Int8ul,
    SolarCharger=0x01,
)

victron_data_parser = Struct(
    "manufacturer_data" / ManufacturerData,
    "record_length" / Int8ul,
    "product_id" / ProductID,
    "record_type" / RecordType,
    "counter_lsb" / Int8ul,
    "counter_msb" / Int8ul,
    "encryption_key_byte_0" / Int8ul,
    "encrypted_data" / GreedyBytes,
)


parsed_data = victron_data_parser.parse(raw_data)

print(hex(parsed_data.encryption_key_byte_0))

print(parsed_data)


# Example usage
hex_bindkey = "xxxx"


decrypted_data = decrypt_message(hex_bindkey, parsed_data.encrypted_data, parsed_data.counter_lsb, parsed_data.counter_msb)

print("Decrypted Data:", decrypted_data)

VE_REG_DEVICE_STATE = Enum(
    Int8ul,
    NOT_CHARGING=0x00,
    UNAVAILABLE=0xFF,
)

VE_REG_CHR_ERROR_CODE = Enum(
    Int8ul,
    NO_ERROR=0x00,
    NA=0xFF,
)

ByteSequenceStructure = Struct(
    "device_state" / VE_REG_DEVICE_STATE,
    "Charger error" / VE_REG_CHR_ERROR_CODE,
    "voltage" / Int16ul,
    "current" / Int16ul,
    "yield" / Int16ul,
    "pv_power" / Int16ul,
    "load_current"
    / BitStruct(  # Load current uses 9 bits
        "load_current_value" / BitsInteger(9),  # Load current is 9 bits wide
        "reserved" / BitsInteger(7),  # Fill up the remaining 7 bits to make up a full byte
    ),
)

# Parse the byte sequence using the structure
parsed_data = ByteSequenceStructure.parse(decrypted_data)

# Output the parsed result
print(parsed_data)
