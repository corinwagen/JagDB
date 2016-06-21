from __future__ import unicode_literals
from django.db import models
#from JagDB.question_categorizer.models import Packet, Subject

class Tossup(models.Model):
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    flagged = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    packet = models.ForeignKey("Packet", related_name="tossup_packet")
    subject = models.ForeignKey("Subject", related_name="tossup_subject")
    tossup_text = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey("AuthUser", related_name="created_by")
    updated_by = models.ForeignKey("AuthUser", related_name="updated_by")

    class Meta:
        managed = False
        db_table = 'tossups'


class Bonus(models.Model):
    leadin = models.TextField(blank=True, null=True)
    part1 = models.TextField(blank=True, null=True)
    answer1 = models.TextField(blank=True, null=True)
    part2 = models.TextField(blank=True, null=True)
    answer2 = models.TextField(blank=True, null=True)
    part3 = models.TextField(blank=True, null=True)
    answer3 = models.TextField(blank=True, null=True)
    flagged = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    packet = models.ForeignKey("Packet", related_name="bonus_packet")
    subject = models.ForeignKey("Subject", related_name="bonus_subject")
    bonus_text = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey("AuthUser", related_name="bonus_created_by")
    updated_by = models.ForeignKey("AuthUser", related_name="bonus_updated_by")

    class Meta:
        managed = False
        db_table = 'bonuses'


