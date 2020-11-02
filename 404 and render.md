## 一个快捷函数： [**get_object_or_404()**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.get_object_or_404)

尝试用 [**get()**](https://docs.djangoproject.com/zh-hans/3.1/ref/models/querysets/#django.db.models.query.QuerySet.get) 函数获取一个对象，如果不存在就抛出 [**Http404**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/views/#django.http.Http404) 错误也是一个普遍的流程。

也有 [**get_list_or_404()**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.get_list_or_404) 函数，工作原理和 [**get_object_or_404()**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 一样，除了 [**get()**](https://docs.djangoproject.com/zh-hans/3.1/ref/models/querysets/#django.db.models.query.QuerySet.get) 函数被换成了 [**filter()**](https://docs.djangoproject.com/zh-hans/3.1/ref/models/querysets/#django.db.models.query.QuerySet.filter) 函数。如果列表为空的话会抛出 [**Http404**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/views/#django.http.Http404) 异常。



### 为什么我们使用辅助函数 [**get_object_or_404()**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 而不是自己捕获 [**ObjectDoesNotExist**](https://docs.djangoproject.com/zh-hans/3.1/ref/exceptions/#django.core.exceptions.ObjectDoesNotExist) 异常呢？还有，为什么模型 API 不直接抛出 [**ObjectDoesNotExist**](https://docs.djangoproject.com/zh-hans/3.1/ref/exceptions/#django.core.exceptions.ObjectDoesNotExist) 而是抛出 [**Http404**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/views/#django.http.Http404) 呢？

因为这样做会增加模型层和视图层的耦合性。指导 Django 设计的最重要的思想之一就是要保证松散耦合。一些受控的耦合将会被包含在 [**django.shortcuts**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#module-django.shortcuts) 模块中。

```python
#不使用快捷函数
from django.http import Http404

from django.shortcuts import render



from .models import Question

\# ...

def detail(request, question_id):

  try:

    question = Question.objects.get(pk=question_id)

  except Question.DoesNotExist:

    raise Http404("Question does not exist")

  return render(request, 'polls/detail.html', {'question': question})
```

```python
#使用快捷函数get_object_or_404()
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```



## 一个快捷函数： [render()](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.render)

「载入模板，填充上下文，再返回由它生成的 [**HttpResponse**](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpResponse) 对象」是一个非常常用的操作流程。



The [**render()**](https://docs.djangoproject.com/zh-hans/3.1/topics/http/shortcuts/#django.shortcuts.render) function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an [**HttpResponse**](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpResponse) object of the given template rendered with the given context.

 不使用render时：

```python
from django.http import HttpResponse

from django.template import loader



from .models import Question



def index(request):

  latest_question_list = Question.objects.order_by('-pub_date')[:5]

   template = loader.get_template('polls/index.html')

  context = {

   'latest_question_list': latest_question_list,

  }

  return HttpResponse(template.render(context, request))
```

使用render函数

```python
from django.shortcuts import render



from .models import Question



def index(request):

  latest_question_list = Question.objects.order_by('-pub_date')[:5]

  context = {'latest_question_list': latest_question_list}

  return render(request, 'polls/index.html', context)
```

