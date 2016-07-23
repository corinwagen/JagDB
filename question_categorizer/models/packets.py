from __future__ import unicode_literals

from django.db import models
#from JagDB.question_categorizer.models import Tournament 

class Packet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    packet_mongo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tournament = models.ForeignKey("Tournament")

    def __unicode__(self):
        return "{}".format(self.name)
    
    class Meta:
        managed = False
        db_table = 'packets'

#
