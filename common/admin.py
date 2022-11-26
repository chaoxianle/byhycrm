from django.contrib import admin
from common.models import CommonCustomer

# Register your models here.

# 在系统中可以看到admin账号
admin.site.register(CommonCustomer)
