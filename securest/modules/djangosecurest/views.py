import os
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CertificateModel, SessionToken

@csrf_exempt
def generate_session_token(request):
	print 'hi'
	cert_id = request.META['HTTP_X_JAG_CERTIFICATEID']

	try:
		url = request.securest_decrypted['url']
	except:
		r = HttpResponse('Required parameter `url` missing.')
		r.status_code = 403
		return r

	token = os.urandom(16).encode('hex') + cert_id
	cert = CertificateModel.objects.get(cert_id=cert_id)
	
	s = SessionToken.objects.filter(certificate=cert, url=url)
	if s.exists():
		s = s[0]
		s.token = token
	else:
		s = SessionToken(certificate=cert, token=token, url=url)
	
	s.save()

	return HttpResponse(token)