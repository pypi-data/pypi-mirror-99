def xor(str, key):
    """Method that performs xor encryption
    
    Keyword arguments:
    str -- text for XOR encryption / decryption
    key -- key for XOR encryption / decryption

    """
    str_encode = ""
    for i in range(0, len(str)):
        str_encode += chr(ord(str[i]) ^ ord(key[i % len(key)]))
    return str_encode