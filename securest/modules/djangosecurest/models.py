from django.db import models

class CertificateModel(models.Model):
	public_key = models.TextField()
	cert_id = models.TextField()
	key_algo = models.CharField(max_length=16)

class SessionToken(models.Model):
	certificate = models.ForeignKey(CertificateModel)
	url = models.TextField()
	token = models.TextField()