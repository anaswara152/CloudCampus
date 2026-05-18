from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class EventManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    semester = models.IntegerField(default=0)
    department = models.CharField(max_length=100)
    student_id=models.FileField(upload_to='proof',default='null')
    registration_no=models.CharField(max_length=100,default='null')
    status=models.CharField(max_length=100,default='pending')

class Event(models.Model):
    event_manager = models.ForeignKey(EventManager, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster=models.FileField(upload_to='poster',null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Programme(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    programme_type = models.CharField(max_length=50)
    min_members = models.IntegerField(default=1)
    max_members = models.IntegerField()
    allowed_song_type = models.CharField(max_length=200,)
    time_limit = models.IntegerField()    

    def __str__(self):
        return self.name
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

