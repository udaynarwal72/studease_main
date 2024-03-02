from django.db import models
# from models import branchDetails

# Create your models here.
# we can understand this as we created a xcel sheet named contact
class contact(models.Model):
    name = models.CharField(max_length=122,default='')
    email = models.CharField(max_length=122,default='')
    date = models.DateField()

    def __str__(self):
        return self.name

class loginDetails(models.Model):
    username = models.CharField(max_length=122,default='')
    password = models.CharField(max_length=122,default='')

    def __str__(self):
        return self.username
    
class branchDetails(models.Model):
    branch = models.CharField(max_length=122,default='')
    section = models.IntegerField(max_length=122,default=0)

    def __str__(self):
        return self.branch

# class timeTable(models.Model):
#     branch =  branchDetails.objects.all()[0].branch
#     section =  branchDetails.objects.all()[0].section