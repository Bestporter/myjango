"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

"""
在软件开发初期，url地址的路径设计可能并不完美，后期需要进行调整，如果项目中很多地方使用了该路径，
一旦该路径发生变化，就意味着所有使用该路径的地方都需要进行修改，这是一个非常繁琐的操作。

解决方案就是在编写一条url(regex, view, kwargs=None, name=None)时，
可以通过参数name为url地址的路径部分起一个别名，项目中就可以通过别名来获取这个路径。
以后无论路径如何变化别名与路径始终保持一致。
通过别名获取路径的过程称为反向解析
"""
# url(regex, view, kwargs=None, name=None)
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
