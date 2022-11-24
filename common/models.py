from django.db import models

# Create your models here.

# 定义客户表
class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200) # CharField = varchar
    #联系电话
    phonenumber = models.CharField(max_length=200)
    #地址
    address = models.CharField(max_length=200)