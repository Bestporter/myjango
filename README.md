Django 如何知道 {% url %} 标签到底对应哪一个应用的 URL 呢？
答案是：在根 URLconf 中添加命名空间。在 polls/urls.py 文件中稍作修改，加上 app_name 设置命名空间：


如何去除模版中的硬编码
将：
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
改成：
问题在于，硬编码和强耦合的链接，对于一个包含很多应用的项目来说，修改起来是十分困难的。然而，因为你在 polls.urls 的 url() 函数中通过 name 参数为 URL 定义了名字，你可以使用 {% url %} 标签代替它：
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>


模板系统
https://docs.djangoproject.com/zh-hans/3.1/topics/templates/
统一使用点符号来访问变量的属性。在示例 {{ question.question_text }} 中，首先 Django 尝试对 question 对象使用字典查找（也就是使用 obj.get(str) 操作），如果失败了就尝试属性查找（也就是 obj.str 操作），结果是成功了。如果这一操作也失败的话，将会尝试列表查找（也就是 obj[int] 操作）。


{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}

question.choice_set.all 被解释为 Python 代码 question.choice_set.all() ，将会返回一个可迭代的 Choice 对象，这一对象可以在 {% for %} 标签内部使用。

一个快捷函数： render()
「载入模板，填充上下文，再返回由它生成的 HttpResponse 对象」是一个非常常用的操作流程。

The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

一个快捷函数： get_object_or_404()
尝试用 get() 函数获取一个对象，如果不存在就抛出 Http404 错误也是一个普遍的流程。
也有 get_list_or_404() 函数，工作原理和 get_object_or_404() 一样，除了 get() 函数被换成了 filter() 函数。如果列表为空的话会抛出 Http404 异常。

为什么我们使用辅助函数 get_object_or_404() 而不是自己捕获 ObjectDoesNotExist 异常呢？还有，为什么模型 API 不直接抛出 ObjectDoesNotExist 而是抛出 Http404 呢？
因为这样做会增加模型层和视图层的耦合性。指导 Django 设计的最重要的思想之一就是要保证松散耦合。一些受控的耦合将会被包含在 django.shortcuts 模块中。


模板命名空间

你的模板文件的路径应该是 polls/templates/polls/index.html，虽然我们现在可以将模板文件直接放在 polls/templates 文件夹中（而不是再建立一个 polls 子文件夹），但是这样做不太好。Django 将会选择第一个匹配的模板文件，如果你有一个模板文件正好和另一个应用中的某个模板文件重名，Django 没有办法 区分 它们。我们需要帮助 Django 选择正确的模板，最好的方法就是把他们放入各自的 命名空间 中，也就是把这些模板放入一个和 自身 应用重名的子文件夹里。


视图的概念

是一类具有相同功能和模版的网页的集合。
比如，在一个博客应用中，你可能会创建如下几个视图：
* 博客首页——展示最近的几项内容。
* 内容“详情”页——详细展示某项内容。
* 以年为单位的归档页——展示选中的年份里各个月份创建的内容。
* 以月为单位的归档页——展示选中的月份里各天创建的内容。
* 以天为单位的归档页——展示选中天里创建的所有内容。
* 评论处理器——用于响应为一项内容添加评论的操作。
而在我们的投票应用中，我们需要下列几个视图：
* 问题索引页——展示最近的几个投票问题。
* 问题详情页——展示某个投票的问题和不带结果的选项列表。
* 问题结果页——展示某个投票的结果。
* 投票处理器——用于响应用户为某个问题的特定选项投票的操作。
在 Django 中，网页和其他内容都是从视图派生而来。每一个视图表现为一个 Python 函数（或者说方法，如果是在基于类的视图里的话）。Django 将会根据用户请求的 URL 来选择使用哪个视图（更准确的说，是根据 URL 中域名之后的部分）。URL模式是URL的一般形式 - 例如: /newsarchive/<year>/<month>/.
为了将 URL 和视图关联起来，Django 使用了 'URLconfs' 来配置。URLconf 将 URL 模式映射到视图。


每个视图必须要做的只有两件事：返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404 。至于你还想干些什么，随便你。你的视图可以从数据库里读取记录，可以使用一个模板引擎（比如 Django 自带的，或者其他第三方的），可以生成一个 PDF 文件，可以输出一个 XML，创建一个 ZIP 文件，你可以做任何你想做的事，使用任何你想用的 Python 库。


Django part3~
ASGI (Asynchronous Server Gateway Interface)  docs，https://asgi.readthedocs.io/en/latest/
WSGI提供是同步的python app的标准，ASGI为异步和同步应用程序提供了一个WSGI向后兼容性实现和多个服务器和应用程序框架。

* 外键关系由 FOREIGN KEY 生成。你不用关心 DEFERRABLE 部分，它只是告诉 PostgreSQL，请在事务全都执行完之后再创建外键关系。


迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。我们会在后面的教程中更加深入的学习这部分内容，现在，你只需要记住，改变模型需要这三步：
* 编辑 models.py 文件，改变模型。
* 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
* 运行 python manage.py migrate 来应用数据库迁移。

使用python manage.py shell 而没选择python命令来直接打开python shell，是因为 manage.py 会设置 DJANGO_SETTINGS_MODULE 环境变量，这个变量会让 Django 根据 mysite/settings.py 文件来设置 Python 包的导入路径。

给模型增加 __str__() 方法是很重要的，这不仅仅能给你在命令行里使用带来方便，Django 自动生成的 admin 里也使用这个方法来表示对象。


但是我们的投票应用在哪呢？它没在索引页面里显示。
只需要再做一件事：我们得告诉管理员，问题 Question 对象需要一个后台接口。打开 polls/admin.py 文件，把它编辑成下面这样：

from django.contrib import admin

from .models import Question

admin.site.register(Question)


当某人请求你网站的某一页面时——比如说， "/polls/34/" ，Django 将会载入 mysite.urls 模块，因为这在配置项 ROOT_URLCONF 中设置了。然后 Django 寻找名为 urlpatterns 变量并且按序匹配正则表达式。在找到匹配项 'polls/'，它切掉了匹配的文本（"polls/"），将剩余文本——"34/"，发送至 'polls.urls' URLconf 做进一步处理。在这里剩余文本匹配了 '<int:question_id>/'，使得我们 Django 以如下形式调用 detail():
detail(request=<HttpRequest object>, question_id=34)
question_id=34 由 <int:question_id> 匹配生成。使用尖括号“捕获”这部分 URL，且以关键字参数的形式发送给视图函数。上述字符串的 :question_id> 部分定义了将被用于区分匹配模式的变量名，而 int: 则是一个转换器决定了应该以什么变量类型匹配这部分的 URL 路径。
  
  URL调度器
https://docs.djangoproject.com/zh-hans/3.1/topics/http/urls/

Database API 
https://docs.djangoproject.com/zh-hans/3.1/topics/db/queries/
Django 创建管理用户
Python manage.py createsuperuser

Question.objects.all()可以查询到这个类的所有对象
Question.objects.filter(id=1) 
Question.objects.filter(question_text__startswith=‘what’)筛选以what开头的  （根据类中的__str__方法返回的名字）
Question.objects.get(pk=1)与get（id=1）相同， pk指primary key

sqlmigrate命令接收一个迁移的名称然后返回对应的SQL
	Python manage.py sqlmigrate polls 0001
请注意以下几点：
* 输出的内容和你使用的数据库有关，上面的输出示例使用的是 PostgreSQL。
* 数据库的表名是由应用名(polls)和模型名的小写形式( question 和 choice)连接而来。（如果需要，你可以自定义此行为。）
* 主键(IDs)会被自动创建。(当然，你也可以自定义。)
* 默认的，Django 会在外键字段名后追加字符串 "_id" 。（同样，这也可以自定义。）
* 外键关系由 FOREIGN KEY 生成。你不用关心 DEFERRABLE 部分，它只是告诉 PostgreSQL，请在事务全都执行完之后再创建外键关系。
* 生成的 SQL 语句是为你所用的数据库定制的，所以那些和数据库有关的字段类型，比如 auto_increment (MySQL)、 serial (PostgreSQL)和 integer primary key autoincrement (SQLite)，Django 会帮你自动处理。那些和引号相关的事情 - 例如，是使用单引号还是双引号 - 也一样会被自动处理。
* 这个 sqlmigrate 命令并没有真正在你的数据库中的执行迁移 - 相反，它只是把命令输出到屏幕上，让你看看 Django 认为需要执行哪些 SQL 语句。这在你想看看 Django 到底准备做什么，或者当你是数据库管理员，需要写脚本来批量处理数据库时会很有用。


改变模型需要三步；
* 编辑 models.py 文件，改变模型。
* 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
* 运行 python manage.py migrate 来应用数据库迁移。
* 
梳理出迁移的操作步骤就不难了。
* 首先在models.py中创建或者修改模型类
* 跑python manager.py makemigrations创建本次修改的迁移文件，此时会去数据库中查找上一次执行的文件并记录在本文件中
* 然后执行python manager.py migrate执行迁移，将变更同步到数据库中
假如某次操作涉及的操作太细碎，迁移后的效果不理想，最好的办法就是回退到上一次迁移的时候。
Django为我们创建了快捷的回退操作，直接对前一步的迁移文件重新手动迁移一次即可完成回退操作。
以上面创建三个表为例，直接再跑python manage.py migrate Four 0003_auto_20200401_2321即可。记得带上Four这个应用名
之后别忘了手动删除migrations目录中的0004号迁移文件，从而完成回退动作。


Django part1 and 2 
2020.10.29日

函数 include() 允许引用其它 URLconfs。每当 Django 遇到 include() 时，它会截断与此项匹配的 URL 的部分，并将剩余的字符串发送到 URLconf 以供进一步处理。


函数 path() 具有四个参数，两个必须参数：route 和 view，两个可选参数：kwargs 和 name。现在，是时候来研究这些参数的含义了
￼

设置DATABASES https://docs.djangoproject.com/zh-hans/3.1/ref/settings/#std:setting-DATABASES
当需要使用sqlite以外的程序的时候需要使用

注：
SQLite 以外的其它数据库
如果你使用了 SQLite 以外的数据库，请确认在使用前已经创建了数据库。你可以通过在你的数据库交互式命令行中使用 "CREATE DATABASE database_name;" 命令来完成这件事。
另外，还要确保该数据库用户中提供 mysite/settings.py 具有 "create database" 权限。这使得自动创建的 test database 能被以后的教程使用。
如果你使用 SQLite，那么你不需要在使用前做任何事——数据库会在需要的时候自动创建。


为了在工程中包含应用需要在主settings中配置INSTALLED_APPS，添加路径，polls.apps.PollsConifg，因为PollsConfig类写着文件polls/apps.py中,然后终端允许python manage.py makemigrations polls，通过允许这个命令，django会检测你对模型文件的修改然后对修改的部分存储为一次迁移。

迁移是 Django 对于模型定义（也就是你的数据库结构）的变化的储存形式 - 它们其实也只是一些你磁盘上的文件。如果你想的话，你可以阅读一下你模型的迁移数据，它被储存在 polls/migrations/0001_initial.py 里。别担心，你不需要每次都阅读迁移文件，但是它们被设计成人类可读的形式，这是为了便于你手动调整Django的修改方式。



