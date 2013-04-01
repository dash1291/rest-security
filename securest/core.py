from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib


"""
`Message` class for creating wrapper objects for REST messages.

Accepts a few required keyword parameters:

* `certificate`: Sender's unique certificate identifier.
* `digest_algo`: Algorithm used to calculate message digest.
* `digest_val`: Value of digest received.
* `key_encypt_algo`: Algorithm used to encrypt the symmetric key, which is
used to encrypt the message.
* `msg_encypt_algo`: Algorithm used to encrypt the message.
* `signature_algo`: Algorithm used to calculate signature value.
* `signature_val`: Signature value.
"""
class Message(object):
    prefix = 'X-JAG-'
    
    def __init__(self, **kwargs):
        self.digest_algo = kwargs['digest_algo']
        self.key_encypt_algo = kwargs['key_encrypt_algo']
        self.msg_encypt_algo = kwargs['msg_encypt_algo']
        self.signature_algo = kwargs['signature_algo']
        self.signature_val = kwargs['signature_val']
        self.digest_val = kwargs['digest_val']
        self.key_encrypted = kwargs['key_encrypted']
        self.url = kwargs['url']
        self.is_request = kwargs['is_request']

        self.headers = kwargs['headers']
        self.payload = kwargs['payload']

        self.certificate = kwargs['certificate']

    """
    Returns a tuple of response message headers and payload.
    """
    def to_message_data():
        headers = self._build_headers()
        return (headers, self.payload)

    def _calculate_signature(self):
        digest = self._calculate_digest()
        public_key = self.target_public_key
        
        if self.signature_algo == 'RSA-SHA1':
            key = RSA.importKey(public_key)
            signature_val = key.encrypt(digest)
        
        return signature_val

    def _calculate_sym_key(self):
        # TODO
        return symmetric_key

    def _calculate_digest(self):
        # TODO
        algo = self.digest_algo

        if algo == 'SHA1':
            payload_hash = hashlib.sha1(self.certificate_id).hexdigest()
            digest_string = payload_hash + self.signature_algo + (
                self.certificate_id)

            # add url to digest if its a request message
            if self.is_request == True:
                digest_string += self.url
                
            digest_val = hashlib.sha1(digest_string).hexdigest()

        return digest_val

    """
    Build and return the message headers dict and payload tuple.
    """
    def _build_headers(self):
        prefix = Message.prefix
        headers = {}
        headers[prefix + 'CertificateId'] = self.certificate_id
        headers[prefix + 'DigestAlg'] = self.digest_alg
        headers[prefix + 'DigestValue'] = self.digest_val
        headers[prefix + 'SigAlg'] = self.signature_algo
        headers[prefix + 'SigValue'] = self.signature_val
        headers[prefix + 'EncAlg'] = self.msg_encypt_algo
        headers[prefix + 'EncKeyAlg'] = self.key_encrypt_algo
        headers[prefix + 'EncKeyValue'] = self.key_encrypted

        return headers


"""
Wrapper class for inbound messages.
"""
class InboundMessage(Message):
    def __init__(self, **kwargs):
        self.url = kwargs['url'] if 'url' in kwargs else ''
        self.local_private_key = kwargs['local_private_key']
        Message.__init__(self, kwargs)

    """
    Verifies if the signature received matches the calculated one.

    Raises an exception, when `signature` is not found as an object variable.
    """
    def verify_signature(self):
        # TODO:FIX decrypt the signature and check with calculated digest
        digest = self._calculate_digest()
        public_key = self.target_public_key
        key = RSA.importKey(self.local_private_key)
        calc_signature = key.decrypt(self.signature_val)
        
        if self.digest_val == key.decrypt(self._calculate_signature()):
            return True
        else:
            return False

    @staticmethod
    def from_message_data(**kwargs):
        prefix = Message.prefix
        headers_dict = kwargs['headers_dict']

        params = {
            'certificate': kwargs['certificate'],
            'digest_algo': headers_dict[prefix + 'DigestAlg'],
            'digest_val': headers_dict[prefix + 'DigestValue'],
            'signature_algo': headers_dict[prefix + 'SigAlg'],
            'signature_val': headers_dict[prefix + 'SigValue'],
            'msg_encrypt_algo': headers_dict[prefix + 'EncAlg'],
            'key_encrypt_algo': headers_dict[prefix + 'EncKeyAlg'],
            'key_encrypted': headers_dict[prefix + 'EncKeyValue'],
            'payload': kwargs['payload'],
            'local_private_key': kwargs['local_private_key'],
            'url': kwargs['url'],
            'is_request': kwargs['is_request']
        }

        return InboundMessage(**params)


"""
Wrapper class for outbound messages.
"""
class OutboundMessage(Message):
    def __init__(self, **kwargs):
        self.remote_public_key = kwargs['remote_public_key']

        # OutboundMessage() doesn't need these values, it will calculate them
        kwargs['signature_val'] = self._calculate_signature()
        kwargs['digest_val'] = self._calculate_digest()
        kwargs['key_encrypted'] = self._calculate_sym_key()

        Message.__init__(self, **kwargs)


"""
Base class for storing certificate data.

Sub-classes must extend the methods `get` and `save`.
"""
class CertificateModel(object):
    def __init__(self, **kwargs):
        self.cert_id = kwargs['cert_id']
        self.key_algo = kwargs['key_algo']

        if 'public_key' in kwargs:
            self.public_key = kwargs['public_key']
        else:
            self.public_key = None

    def _generate_keys():
        # generate RSA keys here
        if self.key_algo == 'RSA-1024':
            randomizer = Random.new().read
            key = RSA.generate(1024, randomizer)
            self.public_key = key.publickey().exportKey()

            # return the private key
            return key.exportKey()

    @staticmethod
    def get(certificate_id):
        raise 'NotImplementedException'

    def save(self):
        # Must return a private key
        raise 'NotImplementedException'


"""
Encrypts a message.
"""
def encrypt(message):
    # encrypt the message
    return Message()

"""
Utility method to decrypt.
"""
def decrypt(message):
    # return Message object after decryption
    return Message()