from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test(request):
	print request.securest_decrypted
	return HttpResponse('hi')

@csrf_exempt
def app_signup(request):
	return HttpResponse('hi')