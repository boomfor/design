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
    cus_wanting_reason = models.CharField(max_length=20,default="",null=True)  #买车原因
    cus_coming_rules = models.CharField(max_length=20,default="",null=True)  #线索来源
    cus_wanting_level =  models.IntegerField(default=0,null=True) #意向等级
    cus_coming_counts = models.IntegerField(default=1,null=True)   #到店次数
    cus_next_following_time = models.DateTimeField(null=True)  #下次接待时间
    cus_coming_time = models.DateTimeField(null=True)  #今日到店
    cus_following_time = models.DateTimeField(null=True)  #接待时间
    cus_first_coming_time = models.DateTimeField(null=True)  #初次到店时间
    cus_treat_counts = models.IntegerField(default=0,null=True)  #接待次数
    cus_adress = models.CharField(max_length=5,default="",null=True)
    cus_budget = models.IntegerField(default=0,null=True)
    cus_sex = models.CharField(max_length=8,default="",null=True)
    cus_avatarurl = models.CharField(max_length=100,default="",null=True)
    cus_creating_time = models.DateTimeField(null=True)
    cus_sign = models.CharField(max_length=20, default="0",null=True)

class Cus_Follow_Record(models.Model):
    open_id = models.CharField(max_length=100, default="", null=True)
    cus_tel_num = models.ForeignKey(Customer,on_delete=models.CASCADE)
    cus_follow_time = models.DateTimeField(primary_key=True)
    cus_next_following_time = models.DateTimeField(null=True)
    cus_wanting_cars = models.CharField(max_length=20, default="", null=True)
    cus_wangting_level =  models.IntegerField(default=0,null=True)
    cus_budget = models.IntegerField(default=0, null=True)  #0低  1偏低  2中 3偏高 4高
    mark = models.TextField(default="",null=True)

class Cus_Sign_Record(models.Model):
    open_id = models.CharField(max_length=100, default="", null=True)
    cus_tel_num = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cus_sign_time = models.DateTimeField(primary_key=True)
    cus_buying_cars = models.CharField(max_length=20, default="", null=True)
    cus_cost = models.IntegerField(default=0, null=True)






