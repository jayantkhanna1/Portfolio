from django.conf.urls import url
from django.db import models

class Education(models.Model):
    name=models.CharField(max_length=100)
    year_from=models.CharField(max_length=20)
    year_too=models.CharField(max_length=20)
    per_got=models.CharField(max_length=30)
    per_total=models.CharField(max_length=30)
    comment=models.CharField(max_length=1000)
class Job(models.Model):
    name=models.CharField(max_length=100)
    year_from=models.CharField(max_length=20)
    year_too=models.CharField(max_length=20)
    place=models.CharField(max_length=100)
    comment=models.CharField(max_length=1000)
class Skills(models.Model):
    name=models.CharField(max_length=100)
    per=models.CharField(max_length=30)
class Accomplishments(models.Model):
    name=models.CharField(max_length=100)
    message=models.CharField(max_length=100)
    img=models.ImageField(upload_to="pics/accomplishments/",null=0)
    likes=models.IntegerField()
    url=models.CharField(max_length=100)
class Privatespace_users(models.Model):
    email=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
class Files(models.Model):
    path=models.FileField(upload_to='files/',null=0)
    filename=models.CharField(max_length=9000)
class Static_website(models.Model):
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    url=models.CharField(max_length=200)
    startdate=models.CharField(max_length=100)
    enddate=models.CharField(max_length=100)
    likes=models.IntegerField()
    img=models.ImageField(upload_to="pics/static_website/",null=0)
    sheetname=models.CharField(max_length=100)
class Fullstack_website(models.Model):
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    url=models.CharField(max_length=200)
    startdate=models.CharField(max_length=100)
    enddate=models.CharField(max_length=100)
    likes=models.IntegerField()
    img=models.ImageField(upload_to="pics/dynamic/",null=0)
    sheetname=models.CharField(max_length=100)
class Animations(models.Model):
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    url=models.CharField(max_length=200)
    startdate=models.CharField(max_length=100)
    enddate=models.CharField(max_length=100)
    likes=models.IntegerField()
    img=models.ImageField(upload_to="pics/animations/",null=0)
    sheetname=models.CharField(max_length=100)