from django.contrib import admin
# we imported contact through this..
from studease.models import contact
from studease.models import loginDetails
from studease.models import branchDetails
# from studease.models import timeTable
# Register your models here.
admin.site.register(contact) #registered our model through this..¸
admin.site.register(loginDetails)
admin.site.register(branchDetails)
# admin.site.register(timeTable)