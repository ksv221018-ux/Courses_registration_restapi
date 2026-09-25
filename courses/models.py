from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    trainer_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.course.course_name
