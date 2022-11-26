from django.db import models
import datetime
# Create your models here.

# # 定义客户表
# class Customer(models.Model):
#     # 客户名称
#     name = models.CharField(max_length=200) # CharField = varchar
#     #联系电话
#     phonenumber = models.CharField(max_length=200)
#     #地址
#     address = models.CharField(max_length=200)
#
# # 定义药品表
# class Medicine(models.Model):
#     # 药品名
#     name = models.CharField(max_length=200)
#     #药品编号
#     sn = models.CharField(max_length=200)
#     #描述
#     desc = models.CharField(max_length=200)
#
# # 定义订单表
# class Order(models.Model):
#     # 订单名
#     name = models.CharField(max_length=200,null=True,blank=True)
#     # 创建日期
#     create_date = models.DateField(default=datetime.datetime.now)
#     # 客户
#     customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
#     # 订单购买的药品
#     medicines = models.ManyToManyField(Medicine,through='OrderMedicine')
#
# # 定义药品的订单表
# class OrderMedicine(models.Model):
#     order = models.ForeignKey(Order,on_delete=models.PROTECT)
#     medicine = models.ForeignKey(Medicine,on_delete=models.PROTECT)
#
#     # 订单中药品的数量
#     amount = models.PositiveIntegerField()
#
# # 导入数据库中所有表
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class CommonCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'common_customer'

class CommonMedicine(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'common_medicine'

class CommonOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateField()
    customer = models.ForeignKey(CommonCustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_order'

class CommonOrdermedicine(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.PositiveIntegerField()
    medicine = models.ForeignKey(CommonMedicine, models.DO_NOTHING)
    order = models.ForeignKey(CommonOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_ordermedicine'

