from django.contrib import admin
from question_categorizer.models import Tossup, Bonus, Subject, Tournament, Packet

# Register your models here.
admin.site.register(Tossup)
admin.site.register(Bonus)
admin.site.register(Subject)
admin.site.register(Tournament)
admin.site.register(Packet)
