from django.db import models

class CertificateModel(models.Model)
	public_key = models.CharField()
	cert_id = models.CharField()