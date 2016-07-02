from __future__ import unicode_literals

from django.db import models

class Tournament(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    power = models.CharField(max_length=1, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    tournament_mongo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tournaments'


