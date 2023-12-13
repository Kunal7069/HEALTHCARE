from django.db import models
from datetime import datetime
class LadleInfo(models.Model):
    name = models.CharField(max_length=100)
    stop_point_no=models.IntegerField()
    stop_point_work=models.CharField(max_length=500)
    min_temp=models.IntegerField()
    max_temp=models.IntegerField()
    turn_around_time=models.IntegerField()

class LadleUpdate(models.Model):
    name = models.CharField(max_length=100)
    start_time=models.CharField(max_length=500)
    stop_points=models.CharField(max_length=500)
    stop_time=models.CharField(max_length=500)

class LadleUpdateRoomWise(models.Model):
    name = models.CharField(max_length=100)
    date= models.DateField(default=datetime.today().date())
    entry_time=models.CharField(max_length=500)
    room=models.CharField(max_length=500)
    exit_time=models.CharField(max_length=500)
    stop_points=models.CharField(max_length=500,default="hii")

class EntriesAdded(models.Model): 
    name = models.CharField(max_length=100)
    date= models.DateField(default=datetime.today().date())
    count = models.IntegerField()