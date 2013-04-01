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
        rm = ResponseMessage.from_response(response_obj.headers,
                response_obj.text, self.server_certificate, )


    """
    Utility method to make a request and return a response.

    This should be used to make most of the requests to the API.
    """
    def make_request(self, url, **kwargs):
        headers = kwargs['headers']
        data = kwargs['data']
        url = url

        rm = RequestMessage.from_request(url, headers, data,
                self.local_certificate, self.server_certificate.public_key,
                self.private_key)

        rm.encrypt()
        (headers, content) = rm.to_request()

        # `response` will contain unprocess/encrypted response.
        response = request.post(url, headers=headers, data=content)
        self._handle_response(response)