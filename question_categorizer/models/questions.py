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

    def type(self):
        return "tossup"

    def flag_question(self):
        self.flagged = "t"
        self.save()
        return 1

    def unflag_question(self):
        self.flagged = "f"
        self.save()
        return 1
   
    def is_flagged(self):
        if self.flagged == "t":
            return True 
        else:
            return False
    
    def objectify(self):
        info = "Packet {} from {}. ".format(self.packet.name, self.packet.tournament)    
        info += "Created on {} by {}. ".format(self.created_at.strftime("%x"), self.created_by)
        info += "Updated on {} by {}. ".format(self.updated_at.strftime("%x"), self.updated_by)
        
        obj  = {
            "text":     self.__unicode__, 
            "subject": self.subject.subject, 
            "id":       self.id, 
            "flagged":  self.is_flagged(), 
            "info":     info, 
            "type":     "tossup",
        }
        return obj

    def __unicode__(self):
        text = "{} <br> ANSWER: {} ".format(self.question.encode("utf-8"), self.answer.encode("utf-8"))
        text = text.replace("<req>", "<strong> <u>")
        text = text.replace("</req>", "</u> </strong>")
        return text

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
    
    def type(self):
        return "bonus"

    def flag_question(self):
        self.flagged = "t"
        self.save()
        return 1

    def unflag_question(self):
        self.flagged = "f"
        self.save()
        return 1
   
    def is_flagged(self):
        if self.flagged == "t":
            return True 
        else:
            return False
    
    def objectify(self):
        info = "Packet {} from {}. ".format(self.packet.name, self.packet.tournament)    
        info += "Created on {} by {}. ".format(self.created_at.strftime("%x"), self.created_by)
        info += "Updated on {} by {}. ".format(self.updated_at.strftime("%x"), self.updated_by)
        
        obj  = {
            "text":     self.__unicode__, 
            "subject": self.subject.subject, 
            "id":       self.id, 
            "flagged":  self.is_flagged(), 
            "info":     info, 
            "type":     "bonus",
        }
        return obj

    def __unicode__(self):
        text = "{} <br>".format(self.leadin.encode("utf-8"))
        text += "[10] {} <br> ANSWER: {} <br>".format(self.part1.encode('utf-8'), self.answer1.encode('utf-8'))
        text += "[10] {} <br> ANSWER: {} <br>".format(self.part2.encode('utf-8'), self.answer2.encode('utf-8'))
        text += "[10] {} <br> ANSWER: {} ".format(self.part3.encode('utf-8'), self.answer3.encode('utf-8'))
        text = text.replace("<req>", "<strong> <u>")
        text = text.replace("</req>", "</u> </strong>")
        return text

    class Meta:
        managed = False
        db_table = 'bonuses'


