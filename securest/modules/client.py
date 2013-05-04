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
        if response_obj.status_code == 200:
            # handle response here (verify, decrypt, etc.)
            rm = InboundMessage.from_message_data(
                    headers_dict=response_obj.headers,
                    payload=response_obj.text.decode('hex'),
                    local_private_key=self.private_key,
                    is_request=False, certificate=self.server_certificate, url='')


            rm.decrypt()
            return rm.to_message_data()
        else:
            return (response_obj.headers, response_obj.text)

    def make_request(self, url, **kwargs):
        request = self.create_request(url, **kwargs)
        return self.send(request)

    """
    Utility method to create request data.

    This is the intermediate method that should be used to prepare the request,
    before sending it using, the `send()` method.
    """
    def create_request(self, url, **kwargs):
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

        return (url, headers, content)

    def send(self, request):
        (url, headers, content) = request
        response = requests.post(url, headers=headers, data=content)
        return self._handle_response(response)