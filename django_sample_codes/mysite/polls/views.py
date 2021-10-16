from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import Question, Choice

# Create your views here.


# In order to create a basic http response, HttpResponse class can be used.
# In order to load a template, loader function can be used.
# In order to fill a template with context, a dict can be passed to it's
# Template object.
def unused_index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context, request))


# render function is a shortcut which takes the request object, template name
# and context dict and returns an HttpResponse object of them.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def unused_detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html', {'question': question})


# get_object_or_404 function is a shortcut which takes a django model and an
# arbitary number of keyword arguments to pass to the get method of the passed
# model and raises Http404 if the requested object doesn't  exist.
# get_list_or_404 function does the same but instead of get method, it uses
# filter method.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    quesion = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': quesion})


# A dictionary like object can be accessed through request.POST to access
# submitted data by a POST request.
# request.GET does the same for GET requests.
# In order to get the url for a view by it's name, reverse function can be
# used; the namespace of the view can be specified in the given name and
# seperated with a colon.
# In order to prevent data being sent twice by hitting the back button, after
# each successful deal with post data, an HttpResponseRedirect should be
# returned.
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question,
                       'error_message': 'You didn\'t select a choice.'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
