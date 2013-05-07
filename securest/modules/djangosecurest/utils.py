import json
import logging

from django.conf import settings
from django.http import HttpResponse

from securest.core import (OutboundMessage, InboundMessage, CertificateModel,
    Message)
from .models import CertificateModel as DjangoDB_model
from .models import SessionToken

logging.basicConfig(level=logging.INFO)

# pull these from django.conf
SECUREST_DB_MODEL = DjangoDB_model
SERVER_CERTIFICATE_ID = settings.SECUREST_SERVER_CERTIFICATE_ID
SERVER_PRIVATE_KEY = settings.SECUREST_PRIVATE_KEY
PROTECT_LIST = settings.SECUREST_PROTECT_LIST


"""
Django middleware to process request and response.

Patches the `request` object by inserting `securest_decrypted` dict which
contains all the request data.
"""
class Middleware(object):
    def __init__(self):
        self.client_certificate = None

    def process_request(self, request):
        #PROTECT_LIST = PROTECT_LIST.append('/session_token/')
        prt_list = PROTECT_LIST + ['/session_token/']
        if not (request.path in prt_list):
            return None

        prefix = 'HTTP_' + Message.prefix
        if not (prefix + 'CERTIFICATEID' in request.META):
            return None

        cert_id = request.META[prefix + 'CERTIFICATEID']
        
        try:
            certificate = DjangoCertificateModel.get(cert_id)
        except:
            certificate = None
            res = HttpResponse('Bad client certificate id.')
            res.status_code = 403
            return res

        self.client_certificate = certificate

        url = request.build_absolute_uri()
        request_msg = InboundMessage.from_message_data(
                        url=request.build_absolute_uri(),
                        headers_dict=request.META, payload=request.body,
                        certificate=certificate,
                        local_private_key=SERVER_PRIVATE_KEY,
                        is_request=True, headers_prefix='HTTP_')

        sig_result = request_msg.verify_signature()
        
        if sig_result == False:
            res = HttpResponse('Bad Signature.')
            res.status_code = 403
            return res
        else:
            request_msg.decrypt()
            (headers, content) = request_msg.to_message_data()

            if not request.path.endswith('/session_token/'):
                try:
                    token_length = 32 + len(cert_id)
                    session_token = content[:token_length]
                    st_obj = SessionToken.objects.get(
                                certificate=certificate.model,
                                url=url,
                                token=session_token)
                except:
                    res = HttpResponse('Bad session token.')
                    res.status_code = 403
                    return res

                content = content[token_length:]
                st_obj.delete()
                logging.info('Request headers %s' % json.dumps(headers))

            request.securest_decrypted = json.loads(content)

    def process_response(self, request, response):
        prt_list = PROTECT_LIST + ['/session_token/']

        if response.status_code == 403:
            return response

        if not (request.path in prt_list):
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

        response.content = encrypted.encode('hex')
        return response


"""
Django ORM model to store certificate data in the database.
"""
class DjangoCertificateModel(CertificateModel):
    def __init__(self, **kwargs):
        CertificateModel.__init__(self, **kwargs)

        if 'model' in kwargs:
            self.model = kwargs['model']

    @staticmethod
    def get(cert_id=None):
        try:
            if cert_id == None:
                # return server's certficate
                cert = globals()['SECUREST_DB_MODEL'].objects.get(
                        cert_id=SERVER_CERTIFICATE_ID)
            else:
                cert = globals()['SECUREST_DB_MODEL'].objects.get(
                        cert_id=cert_id)
        except:
            raise Exception('No certificate exists.')

        return DjangoCertificateModel(cert_id=cert.cert_id,
            public_key=cert.public_key, key_algo=cert.key_algo,
            model=cert)

    def save(self):
        private_key = self._generate_keys()
        cert = globals()['SECUREST_DB_MODEL'](cert_id=self.cert_id,
                public_key=self.public_key, key_algo=self.key_algo)

        self.model = cert
        cert.save()
        return private_key