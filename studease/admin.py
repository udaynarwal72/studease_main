from django.contrib import admin
# we imported contact through this..
from studease.models import contact
from studease.models import SubSection
from studease.models import RollNumber
from studease.models import TimeTable
# from studease.models import timeTable
# Register your models here.
admin.site.register(contact) #registered our model through this..¸
admin.site.register(SubSection)
admin.site.register(RollNumber)
admin.site.register(TimeTable)
