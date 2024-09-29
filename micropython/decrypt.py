import cryptolib

def xor_bytes(a, b):
    """
    XOR two byte arrays of equal length.

    Args:
        a (bytes): First byte array.
        b (bytes): Second byte array.
    
    Returns:
        bytes: The result of XORing the two byte arrays.
    """
    return bytes([x ^ y for x, y in zip(a, b)])

def increment_counter(counter):
    """
    Increment a 16-byte counter in big-endian format.

    Args:
        counter (bytes): A 16-byte counter.
    
    Returns:
        bytes: The incremented 16-byte counter.
    """
    counter_list = list(counter)
    # Increment counter starting from the least significant byte (rightmost)
    for i in range(15, -1, -1):
        counter_list[i] += 1
        if counter_list[i] <= 0xFF:
            break  # If no overflow, stop incrementing
    return bytes(counter_list)

def decrypt_message(key: str, message: bytes, counter_lsb: int, counter_msb: int):
    """
    Decrypt a message using AES-CTR mode simulated with AES-ECB.

    This function simulates AES-CTR mode by encrypting a counter for each block
    of the message using AES-ECB, then XORing the result with the ciphertext
    block to decrypt it.

    Args:
        key (str): Hexadecimal string representing the AES key (16, 24, or 32 bytes).
        message (bytes): The encrypted message (ciphertext).
        counter_lsb (int): Least significant byte of the counter.
        counter_msb (int): Most significant byte of the counter.
    
    Returns:
        bytes: The decrypted message (plaintext).
    """
    # Convert the hex key to bytes (AES requires 16, 24, or 32 bytes key length)
    key_bytes = bytes.fromhex(key)

    # Construct the initial counter (nonce) as a 16-byte value
    counter = bytes([counter_lsb, counter_msb] + [0] * 14)  # 16 bytes total

    # Initialize AES in ECB mode (Mode 1 for AES ECB)
    aes_cipher = cryptolib.aes(key_bytes, 1)  # 1 is for AES ECB mode

    decrypted_message = b""
    block_size = 16
    num_blocks = (len(message) + block_size - 1) // block_size  # Calculate how many blocks to process

    for block_number in range(num_blocks):
        # Encrypt the counter to produce the keystream
        keystream = aes_cipher.encrypt(counter)

        # Get the next block of the message to decrypt
        start = block_number * block_size
        end = min(start + block_size, len(message))
        message_block = message[start:end]

        # XOR the keystream with the ciphertext block to decrypt
        decrypted_block = xor_bytes(keystream[:len(message_block)], message_block)
        decrypted_message += decrypted_block

        # Increment the counter for the next block
        counter = increment_counter(counter)

    return decrypted_message

if __name__ == "__main__":
    # Test the decryption with known values
    key = "xxx"
    enc = b'xxx'
    lsb = 47
    msb = 48
    correct = b'xxx'

    # Perform the decryption
    dec = decrypt_message(key, enc, lsb, msb)

    # Check if the decryption result matches the expected correct value
    assert dec == correct, f"Decryption failed! Expected: {correct}, but got: {dec}"

    # Print the result of the assertion check
    print("Decryption successful:", dec == correct)



