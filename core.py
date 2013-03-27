"""
`Message` class for creating wrapper objects for REST messages.

Accepts a few required keyword parameters:

* `certificate_id`: Sender's unique certificate identifier.
* `digest_algo`: Algorithm used to calculate message digest.
* `digest_val`: Value of digest received.
* `key_encypt_algo`: Algorithm used to encrypt the symmetric key, which is used
to encrypt the message.
* `msg_encypt_algo`: Algorithm used to encrypt the message.
* `signature_algo`: Algorithm used to calculate signature value.
* `signature_val`: Signature value.
"""
class Message(object):
    def __init__(self, **kwargs):
        self.certificate_id = kwargs['certificate_id']
        self.digest_algo = kwargs['digest_algo']
        self.key_encypt_algo = kwargs['key_encrypt_algo']
        self.msg_encypt_algo = kwargs['msg_encypt_algo']
        self.signature_algo = kwargs['signature_algo']

        self.headers = kwargs['headers']
        self.payload = kwargs['payload']

        if 'digest_val' in kwargs:
            self.digest_val = kwargs['digest_val']
        else:
            self.digest_val = self._calculate_digest(params)

        if 'signature_val' in kwargs:
            self.signature_val = kwargs['signature_val']
        else:
            self.signature_val = self._calculate_signature(params)

        if 'key_encrypted' in kwargs:
            self.signature_val = kwargs['key_encrypted']
        else:
            self.key_encrypted = self._calculate_sym_key(params)


    """
    Verifies if the signature received matches the calculated one.

    Raises an exception, when `signature` is not found as an object variable.
    """
    def verify_signature(self):
        # TODO

    def _calculate_signature(self, **kwargs):
        # TODO

    def _calculate_sym_key(self, **kwargs):
        # TODO

    def _calculate_digest(self, **kwargs):
        # TODO

    """
    Build and return a headers dict for the message.
    """
    def to_headers(self):
        return ''

    """
    Create a `Message` instance from headers supplied.
    """
    @staticmethod
    def from_headers(headers_dict):
        return Message()


"""
Encrypts a message.
"""
def encrypt(self):
    # encrypt the message and return a dict

"""
Utility method to decrypt.
"""
def decrypt(message_dict):
    # return Message object after decryption