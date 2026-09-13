import base64


def XOR_bytes (data: bytes, key: bytes) -> bytes: 
    """ Perform a bitwise XOR operation on the given data using the given key.
    
    Parameters: 
    data (bytes): The data to do the operation on.
    key (bytes): The key used for the operation on the data.
    
    Returns:
    bytes: the operated data.
    """

    # iterates through every data byte into b and i and peroms a XOR operation against the key
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def encode(payload: str, key: str) -> str:
    """ encode payload with the given key.
    
    Parameters:
    payload (str): the payload to encode.
    key (str): the key used to encode the payload.
    
    Returns: 
    str: the encoded string.
    """

    raw = payload.encode("utf-8") 
    xored = XOR_bytes(raw, key.encode("utf-8"))
    return base64.b64encode(xored).decode("ascii")

def decode (encoded: str, key: str) -> str:
    """ decode payload with the given key.
        
    Parameters:
    encoded (str): the payload to decode.
    key (str): the key used to decode the payload.
        
    Returns: 
    str: the decoded string.
    """
    xored = base64.b64decode(encoded)
    raw = XOR_bytes(xored, key.encode("utf-8"))
    return raw.decode("utf-8")


