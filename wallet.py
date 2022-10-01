from re import S
from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def load_keys(self):
        pass

    def generate_keys(self):
        # they only work together
        private_key = RSA.generate(1024, Crypto.Radndom.new().read)
        public_key = private_key.publickey()
        # convert from binary - DER - binary encoding to hexify turns hexa decimal -> convert to ascii
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), public_key.exportKey(format='DER').decode('ascii'))
