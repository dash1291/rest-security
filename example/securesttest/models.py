from django.db import models

class UserModel(models.Model):
	userid = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)