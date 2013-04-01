import json
import requests

from securest.core import CertificateModel, RequestMessage, ResponseMessage


"""
Client side wrapper for interacting with the securest API.
"""
class SecurestClient(object):
    def __init__(self, **kwargs):
        self.local_certificate = CertificateModel(
            public_key=kwargs['client_public_key'],
            cert_id=kwargs['client_certificate_id'])

        self.server_certificate = CertificateModel(
            public_key=kwargs['server_public_key'],
            cert_id=kwargs['server_certificate_id'])

        self.private_key = kwargs['private_key']

    def _handle_response(self, response_obj):
        # handle response here (verify, decrypt, etc.)
        rm = InboundMessage.from_message_data(headers_dict=response_obj.headers,
                payload=response_obj.text, local_private_key=self.private_key,
                is_request=False, certificate=self.server_certificate)

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
            'is_request': True)
        }

        rm = OutboundMessage(**params)

        rm.encrypt()
        (headers, content) = rm.to_message_data()

        # `response` will contain unprocess/encrypted response.
        response = request.post(url, headers=headers, data=content)
        return self._handle_response(response)