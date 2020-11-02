from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# from django.http import HttpResponse
# from django.template import loader
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

'''我们在这里使用两个通用视图： ListView 和 DetailView 。
这两个视图分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念。'''


class IndexView(generic.ListView):
    """使用template_name来告诉ListView使用我们创建的已经存在的"polls/index.html"模板。"""

    template_name = 'polls/index.html'
    '''ListView，自动生成的context变量是question_list。为了覆盖这个行为，我们提供context_object_name
    属性，表示我们想使用latest_question_list。'''
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # lte  : less than or equal
        #Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date is
        # less than or equal to - that is, earlier than or equal to - timezone.now.
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # 每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供。
    model = Question

    # 默认情况下，通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板。
    # template_name 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字。
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


'''
def index(request):

'在之前的教程中，提供模板文件时都带有一个包含 question 和 latest_question_list 变量的 context。\
对于 DetailView ， question 变量会自动提供—— 因为我们使用 Django 的模型 (Question)， 
Django 能够为 context 变量决定一个合适的名字。然而对于 ListView，
 自动生成的 context 变量是 question_list。为了覆盖这个行为，
 我们提供 context_object_name 属性，表示我们想使用 latest_question_list。
 作为一种替换方案，你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，告诉 Django 使用你想使用的变量名。'
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #output = ', '.join([q.question_text for q in latest_question_list])
    return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context,request))
    #return HttpResponse("Hello, world. you're at the polls index.")


def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    #response = "You're looking at the results of question %s."
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # return HttpResponse(response % question_id)


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html',  {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    pass
'''
'''
request.POST 是一个类字典对象，让你可以通过 关键字  的名字获取提交的数据。 这个例子中， request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID。 request.POST 的值永远是字符串。

注意，Django 还以同样的方式提供 request.GET 用于访问 GET 数据 —— 但我们在代码中显式地使用 request.POST ，以保证数据只能通过 POST 调用改动。

如果在 request.POST['choice'] 数据中没有提供 choice ， POST 将引发一个 KeyError 。上面的代码检查 KeyError ，如果没有给出 choice 将重新显示 Question 表单和一个错误信息。

在增加 Choice 的得票数之后，代码返回一个 HttpResponseRedirect 而不是常用的 HttpResponse 、 HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL（请继续看下去，我们将会解释如何构造这个例子中的 URL）。

As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing with POST data. This tip isn't specific to Django; it's good Web development practice in general.

在这个例子中，我们在 HttpResponseRedirect 的构造函数中使用 reverse() 函数。这个函数避免了我们在视图函数中硬编码 URL。它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL 模式中需要给该视图提供的参数。 在本例中，使用在 教程第 3 部分 中设定的 URLconf， reverse() 调用将返回一个这样的字符串：

'/polls/3/results/'
其中 3 是 question.id 的值。重定向的 URL 将调用 'results' 视图来显示最终的页面。
'''
