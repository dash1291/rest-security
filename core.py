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
        self.signature_val = kwargs['signature_val']
        self.digest_val = kwargs['digest_val']
        self.key_encrypted = kwargs['key_encrypted']

        self.headers = kwargs['headers']
        self.payload = kwargs['payload']

    """
    Verifies if the signature received matches the calculated one.

    Raises an exception, when `signature` is not found as an object variable.
    """
    def verify_signature(self):
        if self.signature_val == self._calculate_signature():
            return True
        else:
            return False

    def _calculate_signature(self, **kwargs):
        # TODO
        return signature_val

    def _calculate_sym_key(self, **kwargs):
        # TODO
        return symmetric_key

    def _calculate_digest(self, **kwargs):
        # TODO
        return digest_val

    """
    Build and return the message headers dict and payload tuple.
    """
    def _build_headers(self):
        prefix = 'X-JAG-'
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
Wrapper class for requests messages.
"""
class RequestMessage(Message):
    def __init__(self, **kwargs):
        self.target_url = kwargs['target_url']
        Message.__init__(self, kwargs)

    @staticmethod
    def from_request(url, headers_dict, payload):
        prefix = 'X-JAG-'

        return RequestMessage(certificate_id=headers_dict[prefix + 'CertificateId'],
            digest_algo = headers_dict[prefix + 'DigestAlg'],
            digest_val = headers_dict[prefix + 'DigestValue'],
            signature_algo = headers_dict[prefix + 'SigAlg'],
            signature_val = headers_dict[prefix + 'SigValue'],
            msg_encrypt_algo = headers_dict[prefix + 'EncAlg'],
            key_encrypt_algo = headers_dict[prefix + 'EncKeyAlg'],
            key_encrypted = headers_dict[prefix + 'EncKeyValue'],
            payload=payload, url=url)


"""
Wrapper class for response messages.
"""
class ResponseMessage(Message):
    def __init__(self, **kwargs):
        kwargs['signature_val'] = self._calculate_signature()
        kwargs['digest_val'] = self._calculate_digest()
        kwargs['key_encrypted'] = self._calculate_sym_key()

        Message.__init__(self, **kwargs)

    """
    Returns a tuple of response message headers and payload.
    """
    def to_response():
        headers = self._build_headers()
        return (headers, self.payload)

    @staticmethod
    def from_response(headers_dict, payload):
        prefix = 'X-JAG-'

        return ResponseMessage(certificate_id=headers_dict[prefix + 'CertificateId'],
            digest_algo = headers_dict[prefix + 'DigestAlg'],
            digest_val = headers_dict[prefix + 'DigestValue'],
            signature_algo = headers_dict[prefix + 'SigAlg'],
            signature_val = headers_dict[prefix + 'SigValue'],
            msg_encrypt_algo = headers_dict[prefix + 'EncAlg'],
            key_encrypt_algo = headers_dict[prefix + 'EncKeyAlg'],
            key_encrypted = headers_dict[prefix + 'EncKeyValue'],
            payload=payload)


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