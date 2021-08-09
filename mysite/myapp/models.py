from django.db import models
from django.core.validators import (MinLengthValidator,MaxLengthValidator,MinValueValidator,MaxValueValidator)



branches=(
    ('CSE','CSE'),('ECE','ECE'),('EEE','EEE'),('IT','IT')
)

batches =(
    ('2022','2022'),('2023','2023'),('2024','2024')
)

hosts = (
    ('HACKER_RANK','HACKER_RANK'),('HACKER_EARTH','HACKER_EARTH'),('CODESHEF','CODESHEF'),('SPOJ','SPOJ')
)



class OnlineJudge(models.Model):
    host = models.CharField(max_length=20,choices=hosts)
    username = models.CharField(max_length=20)
    rank = models.IntegerField(editable=True)
    stars = models.IntegerField(editable=True)
    score = models.IntegerField(editable=True)
    user_id = models.CharField(max_length=50,primary_key=True)
    last_edited = models.DateField(auto_now=False,editable=True,null=True)
    is_blocked = models.BooleanField(default=False,editable=True)

    def __str__(self):
        return self.user_id

    def save(self,**kwargs):
        self.user_id = self.username+self.host
        super().save(**kwargs)

class UserModel(models.Model):
    username = models.CharField(max_length=40,unique=True,
    editable=True,validators=[ MaxLengthValidator(15, message='Username is too long'),MinLengthValidator( 6,message='Username is too short')])
    roll_number = models.CharField(max_length=11,
    validators=[MaxLengthValidator(11,message='Username is too long'),MinLengthValidator(10,message='Username is too short..')])
    email = models.EmailField(max_length=200)
    branch = models.CharField(max_length=4,choices=branches)
    yop = models.CharField(max_length=4,choices=batches)
    password = models.CharField(max_length=10,default='password',editable=True)
    accounts = models.ManyToManyField(OnlineJudge)
    is_blocked = models.BooleanField(default=False,editable=True)

    def __str__(self):
        return self.username

    def authenticate(self,password):
        return self.password==password


class MyAdmin(models.Model):

    username = models.CharField(max_length=40,unique=True,editable=True,
	validators=[MaxLengthValidator(15,message='Username is too long'),MinLengthValidator(6,message='Username is too short..')])
    password = models.CharField(max_length=10,default='password',editable=True)

    def __str__(self):
        return self.username



