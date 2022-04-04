from django.db import models


class BA(models.Model):
    type = models.CharField(max_length=20)
    year = models.IntegerField(blank=False, null=False,)
    iterator = models.IntegerField(blank=False, null=False)
