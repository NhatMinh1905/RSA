import rsa

def generate_keys():
    pub, priv = rsa.newkeys(2048)
    return pub.save_pkcs1(), priv.save_pkcs1()

def sign_file(filepath, private_key_bytes):
    priv = rsa.PrivateKey.load_pkcs1(private_key_bytes)
    with open(filepath, "rb") as f:
        data = f.read()
    return rsa.sign(data, priv, 'SHA-256')

def verify_signature(filepath, signature, public_key_bytes):
    pub = rsa.PublicKey.load_pkcs1(public_key_bytes)
    with open(filepath, "rb") as f:
        data = f.read()
    try:
        rsa.verify(data, signature, pub)
        return True
    except:
        return False