from django.http import HttpResponse

from .models import Question

# Create your views here.


# In order to create a basic http response, HttpResponse class can be used.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return HttpResponse(
        ', '.join([q.question_text for q in latest_question_list]))


def detail(request, question_id):
    return HttpResponse(f'You\'re looking at question number {question_id}')


def results(request, question_id):
    response = f'You\'r looking at the results of question {question_id}'
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f'You\'re voting on question {question_id}')
