"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

# In order to refrence other URLconfs, include function can be used. When
# django is encountered with an include, the matched part of the URL is chopped
# off and the rest of it is passed to the included URLconf. The ability of plug
# and play urls is provided by include function. it is typically used for
# external URLconfs (except admin.site.urls).
# The path function can be given four arguments, described as below:
# route (required): a str which contains a url pattern
# when django is searching for url patterns, it doesn't care about GET or POST
# parameters.
# view (required): the view which is called when it's associated url pattern is
# matched. it is called with an HttpRequest object as the first argument and
# any captured values from the pattern as kwargs.
# kwargs (optional)
# name (optional): given so the url can be refrenced from elsewhere. useful to
# avoid redundency.
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
