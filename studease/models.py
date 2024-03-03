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
    roll_number = models.CharField(max_length=100)

class TimeTable(models.Model):
    roll_number = models.ForeignKey(RollNumber, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    day = models.CharField(max_length=50)
    time = models.TimeField()