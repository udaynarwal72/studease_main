from django.db import models
# from models import branchDetails

# Create your models here.
# we can understand this as we created a xcel sheet named contact
class contact(models.Model):
    name = models.CharField(max_length=122,default='')
    email = models.CharField(max_length=122,default='')
    # date = models.DateField()

    def __str__(self):
        return self.name
    
class SubSection(models.Model):
    sub_section_name = models.CharField(max_length=100,default='')

class RollNumber(models.Model):
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE)
    roll_number = models.IntegerField(max_length=100)
    username = models.CharField(max_length=100,default='')

# class TimeTable(models.Model):
#     sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE,default='') # type: ignore
#     # roll_number = models.ForeignKey(RollNumber, on_delete=models.CASCADE)
#     period= models.CharField(max_length=100,default='')
#     monday = models.CharField(max_length=100,default='')
#     tuesday = models.CharField(max_length=100,default='')
#     wednesday = models.CharField(max_length=100,default='')
#     thursday = models.CharField(max_length=100,default='')
#     friday = models.CharField(max_length=100,default='')
#     time = models.TimeField(max_length=8,default="00:00:00") # type: ignore
#     newtime=models.TimeField(max_length=8,default="00:00:00") # type: ignore

class TimeTable(models.Model):
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE, default=None, null=True)
    period = models.CharField(max_length=100, default='')
    monday = models.CharField(max_length=100, default='')
    tuesday = models.CharField(max_length=100, default='')
    wednesday = models.CharField(max_length=100, default='')
    thursday = models.CharField(max_length=100, default='')
    friday = models.CharField(max_length=100, default='')
    time = models.TimeField(default="00:00:00", null=True) # type: ignore
    newtime = models.TimeField(default="00:00:00", null=True) # type: ignore


class userfeedbacktable(models.Model):
    feedbackfirstname=models.CharField(max_length=100)
    feedbacklastname=models.CharField(max_length=100)
    feedbackemail= models.CharField(max_length=100)
    feedbackmessage=models.CharField(max_length=100)
    def __str__(self):
        return self.feedbackemail