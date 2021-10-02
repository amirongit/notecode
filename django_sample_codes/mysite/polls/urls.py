from django.urls import path

from . import views

# In order for a view function to be called, it should be mapped to a url in
# URLconf.
urlpatterns = [
    path('', views.index, name='index'),
]
