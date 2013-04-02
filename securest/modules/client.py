import json
import requests

from securest.core import CertificateModel, InboundMessage, OutboundMessage


"""
Client side wrapper for interacting with the securest API.
"""
class SecurestClient(object):
    def __init__(self, **kwargs):
        self.local_certificate = CertificateModel(
            public_key=kwargs['client_public_key'],
            cert_id=kwargs['client_certificate_id'],
            key_algo='RSA')

        self.server_certificate = CertificateModel(
            public_key=kwargs['server_public_key'],
            cert_id=kwargs['server_certificate_id'],
            key_algo='RSA')

        self.private_key = kwargs['private_key']

    def _handle_response(self, response_obj):
        # handle response here (verify, decrypt, etc.)
        rm = InboundMessage.from_message_data(headers_dict=response_obj.headers,
                payload=response_obj.text.decode('base64'), local_private_key=self.private_key,
                is_request=False, certificate=self.server_certificate, url='')


        rm.decrypt()
        return rm.to_message_data()

    """
    Utility method to make a request and return a response.

    This should be used to make most of the requests to the API.
    """
    def make_request(self, url, **kwargs):
        headers = kwargs['headers']
        data = kwargs['data']

        params = {
            'certificate': self.local_certificate,
            'digest_algo': 'SHA1',
            'signature_algo': 'RSA-SHA1',
            'msg_encrypt_algo': 'AES',
            'key_encrypt_algo': 'RSA',
            'payload': data,
            'remote_public_key': self.server_certificate.public_key,
            'url': url,
            'is_request': True,
            'headers': headers 
        }

        rm = OutboundMessage(**params)

        rm.encrypt()
        (headers, content) = rm.to_message_data()

        # `response` will contain unprocess/encrypted response.
        response = requests.post(url, headers=headers, data=content)
        return self._handle_response(response)