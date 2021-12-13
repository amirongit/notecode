from django.urls import path

from . import views

# In order to create a name space for the url tag in django templates, app_name
# variable can be set.
app_name = 'polls'
# In order for a view function to be called, it should be mapped to a url in
# URLconf.
# In order to capture a part of the url as a kwarg in a view, angle brackets
# can be used in it's associated urlpattern.the expression in angle brackets
# should be like <convertor:var_name>.
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
