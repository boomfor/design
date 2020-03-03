from django.db import models

# Create your models here.
class User(models.Model):
    open_id = models.CharField(max_length=100,unique=True,primary_key=True)
    user_name = models.CharField(max_length=20)
    avatar_url = models.CharField(max_length=200)
    tel_num = models.CharField(max_length=20,default="")


class Customer(models.Model):
    open_id = models.CharField(max_length=100,default="",null=True)
    cus_tel_num = models.CharField(max_length=20,primary_key=True)
    cus_name = models.CharField(max_length=100,default="",null=True)
    cus_nickname = models.CharField(max_length=20,default="",null=True)
    cus_wanting_cars = models.CharField(max_length=20,default="",null=True)
    cus_wanting_reason = models.CharField(max_length=15,default="",null=True)
    cus_wanting_level = models.CharField(max_length=3,default="",null=True)
    cus_following_counts = models.IntegerField(default=0,null=True)
    cus_coming_counts = models.IntegerField(default=1,null=True)
    cus_next_following_time = models.DateTimeField(default="",null=True)
    cus_coming_time = models.DateTimeField(default="",null=True)
    cus_following_days = models.IntegerField(default=0,null=True)
    cus_treat_coounts = models.IntegerField(default=0,null=True)
    cus_adress = models.CharField(max_length=5,default="",null=True)
    cus_budget = models.CharField(max_length=10,default="",null=True)
    cus_sex = models.CharField(max_length=8,default="",null=True)
    cus_avatarurl = models.CharField(max_length=100,default="",null=True)






