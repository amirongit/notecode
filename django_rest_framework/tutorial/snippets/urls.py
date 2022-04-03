from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

# format_suffix_patterns can be used to apply optional formatting options to
# the endpoints, it uses the format kwarg of the view callable.

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)
