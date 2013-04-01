from django.conf import settings
from django.http import HttpResponse

from securest.core import OutboundMessage, InboundMessage, CertificateModel
from .models import CertificateModel as DjangoDB_model


# pull these from django.conf
SECUREST_DB_MODEL = DjangoDB_model
SERVER_PUBLIC_KEY = settings.SECUREST_SERVER_PUBLIC_KEY
SERVER_PRIVATE_KEY = settings.SECUREST_PRIVATE_KEY


"""
Django middleware to process request and response.
"""
class Middleware():
    def process_request(self, request):
        cert_id = request.headers[Message.prefix + 'CertificateId']
        certificate = DjangoCertificateModel.get(cert_id)
        self.client_certificate = certficate

        request_msg = InboundMessage.from_message_data(url=request.url,
            headers_dict=request.headers, payload=request.form,
            certificate=certificate, local_private_key=SERVER_PRIVATE_KEY)

        if request_msg._verify_signature() == False:
            return HttpResponse(error)
        else:
            request_msg.decrypt()
            (headers, content) = request_msg.to_message_data()
            request.headers = headers
            request.form = content

    def process_response(self, request, response):
        server_cert = DjangoCertificateModel.get()

        params = {
            'certificate': self.local_certificate,
            'digest_algo': 'SHA1',
            'signature_algo': 'RSA-SHA1',
            'msg_encrypt_algo': 'AES',
            'key_encrypt_algo': 'RSA',
            'payload': data,
            'remote_public_key': self.client_certificate.public_key,
            'is_request': False)
        }

        response_msg = OutboundMessage(**params)
        response_msg.encrypt()

        (headers, encrypted) = response_msg.to_message_data()
        
        # insert headers fetched above into the response headers
        # and replace the content with above encrypted content.
        response.headers += headers
        response.content = encrypted
        
        return response


"""
Django ORM model to store certificate data in the database.
"""
class DjangoCertificateModel(CertificateModel):
    def __init__(self, **kwargs):
        CertificateModel.__init__(self, **kwargs)

    @staticmethod
    def get(cert_id):
        if cert_id == None:
            # return server's certficate
            cert = globals()['SECUREST_DB_MODEL'].get(id=0)
        else:
            cert = globals()['SECUREST_DB_MODEL'].get(cert_id=cert_id)
        
        return DjangoCertificateModel(cert_id=cert.cert_id,
            public_key=cert.public_key)

    def save():
        private_key = self._generate_keys()
        cert = globals()['SECUREST_DB_MODEL'](cert_id=self.cert_id,
            public_key=self.public_key)

        cert.save()
        return private_key