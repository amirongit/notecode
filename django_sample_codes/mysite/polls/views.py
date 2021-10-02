from django.http import HttpResponse

# Create your views here.


# In order to create a basic http response, HttpResponse class can be used.
def index(request):
    return HttpResponse('Hello, world! Your at the polls index.')
