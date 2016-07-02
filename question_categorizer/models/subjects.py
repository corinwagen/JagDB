from __future__ import unicode_literals

from django.db import models

class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'


