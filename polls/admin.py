from django.contrib import admin
#我们得告诉管理员，问题 Question 对象需要一个后台接口。
# Register your models here.
from django.contrib import admin

from .models import Question

admin.site.register(Question)