from django.db import models
from django.contrib.auth.models import User
from event_manager.models import Event,Programme
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    student_id=models.FileField(upload_to='proof',default='null')
    registration_no=models.CharField(max_length=100,default='null')
    status=models.CharField(max_length=100,default="pending")



class ProgrammeParticipation(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100, blank=True)
    song_name = models.CharField(max_length=200)
    members_count = models.IntegerField()
    status = models.CharField(max_length=50,default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)



class CampusGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Student)
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMessage(models.Model):
    group = models.ForeignKey(CampusGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    
