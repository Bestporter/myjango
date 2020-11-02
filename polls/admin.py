# 我们得告诉管理员，问题 Question 对象需要一个后台接口。
# Register your models here.
from django.contrib import admin

from .models import Question, Choice

'''
你需要遵循以下流程——
创建一个模型后台类，
接着将其作为第二个参数传给 admin.site.register() ——在你需要修改模型的后台管理选项时这么做。
'''


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fieldsets 元组中的第一个元素是字段集的标题
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
