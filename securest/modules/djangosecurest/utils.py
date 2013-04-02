import json

from django.conf import settings
from django.http import HttpResponse

from securest.core import (OutboundMessage, InboundMessage, CertificateModel,
    Message)
from .models import CertificateModel as DjangoDB_model

# pull these from django.conf
SECUREST_DB_MODEL = DjangoDB_model
SERVER_CERTIFICATE_ID = settings.SECUREST_SERVER_CERTIFICATE_ID
SERVER_PRIVATE_KEY = settings.SECUREST_PRIVATE_KEY
PROTECT_LIST = settings.SECUREST_PROTECT_LIST


"""
Django middleware to process request and response.
"""
class Middleware(object):
    def __init__(self):
        self.client_certificate = None

    def process_request(self, request):
        if not (request.path in PROTECT_LIST):
            return None

        prefix = 'HTTP_' + Message.prefix

        if not (prefix + 'CERTIFICATEID' in request.META):
            return None

        cert_id = request.META[prefix + 'CERTIFICATEID']
        certificate = DjangoCertificateModel.get(cert_id)
        self.client_certificate = certificate

        request_msg = InboundMessage.from_message_data(url=request.path,
            headers_dict=request.META, payload=request.body,
            certificate=certificate, local_private_key=SERVER_PRIVATE_KEY,
            is_request=True)

        if request_msg.verify_signature() == False:
            return HttpResponse(error)
        else:
            request_msg.decrypt()
            (headers, content) = request_msg.to_message_data()

            request.securest_decrypted = json.loads(content)

    def process_response(self, request, response):
        if not (request.path in PROTECT_LIST):
            return None

        server_cert = DjangoCertificateModel.get()

        params = {
            'certificate': server_cert,
            'digest_algo': 'SHA1',
            'signature_algo': 'RSA-SHA1',
            'msg_encrypt_algo': 'AES',
            'key_encrypt_algo': 'RSA',
            'payload': response.content,
            'remote_public_key': self.client_certificate.public_key,
            'is_request': False,
            'url': '',
            'headers': {},
        }

        response_msg = OutboundMessage(**params)

        response_msg.encrypt()
        (headers, encrypted) = response_msg.to_message_data()
        
        # insert headers fetched above into the response headers
        # and replace the content with above encrypted content.
        for key in headers.keys():
            response[key] = headers[key]

        response.content = encrypted.encode('base64')
        print 'hi'
        return response


"""
Django ORM model to store certificate data in the database.
"""
class DjangoCertificateModel(CertificateModel):
    def __init__(self, **kwargs):
        CertificateModel.__init__(self, **kwargs)

    @staticmethod
    def get(cert_id=None):
        try:
            if cert_id == None:
                # return server's certficate
                cert = globals()['SECUREST_DB_MODEL'].objects.get(
                    cert_id=SERVER_CERTIFICATE_ID)
            else:
                cert = globals()['SECUREST_DB_MODEL'].objects.get(cert_id=cert_id)
        except:
            raise Exception('No certificate exists.')

        return DjangoCertificateModel(cert_id=cert.cert_id,
            public_key=cert.public_key, key_algo=cert.key_algo)

    def save(self):
        private_key = self._generate_keys()
        cert = globals()['SECUREST_DB_MODEL'](cert_id=self.cert_id,
            public_key=self.public_key, key_algo=self.key_algo)

        cert.save()
        return private_key