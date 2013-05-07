import json
import logging

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from .models import UserModel

logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def test(request):
	logging.info('Payload data in the view (decrypted): %s' % json.dumps(
		request.securest_decrypted))
	return HttpResponse('hello world!')

@csrf_exempt
def app_signup(request):
	return HttpResponse('hi')

@csrf_exempt
def register_user(request):
	data = request.securest_decrypted
	new_user = UserModel(first_name=data['first_name'],
		last_name=data['last_name'])

	new_user.save()
	return HttpResponse('User has been added.')