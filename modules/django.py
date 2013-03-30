from django.http import HttpResponse

from securest.core import ResponseMessage, RequestMessage, CertificateModel

DB_MODEL = 'django-database-model-class-here'
PUBLIC_KEY = ''

class Middleware():
	def process_request(self, request):
		cert_id = request.headers[Message.prefix + 'CertificateId']
		certificate = DjangoCertificateModel.get(cert_id)
		self.client_certificate = certficate

		request_msg = RequestMessage.from_request(request.url,
			request.headers, request.form, certificate, PUBLIC_KEY)

		if request._verify_signature() == False:
			return HttpResponse(error)

	def process_response(self, request, response):
		server_cert = DjangoCertificateModel.get()
		response_msg = ResponseMessage.from_response(response.headers,
			response_content, server_cert, self.client_certificate.public_key)
		(headers, encrypted) = response_msg.to_response()
		
		# insert headers fetched above into the response headers
		# and replace the content with above encrypted content.
		response.headers

class DjangoCertificateModel(CertificateModel):
	def __init__(self, **kwargs):
		CertificateModel.__init__(self, **kwargs)

	@staticmethod
	def get(cert_id):
		if cert_id == None:
			# return server's certficate
			cert = global()['DB_MODEL'].get(id=0)
		else:
			cert = global()['DB_MODEL'].get(cert_id=cert_id)
		
		return DjangoCertificateModel(cert_id=cert.cert_id,
			public_key=cert.public_key,
			private_key=cert.private_key)

	def save():
		cert = global()['DB_MODEL'](cert_id=self.cert_id,
			public_key=public_key, private_key=private_key)

		cert.save()