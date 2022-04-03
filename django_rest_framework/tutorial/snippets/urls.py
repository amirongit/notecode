from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

# format_suffix_patterns can be used to apply optional formatting options to
# the endpoints, it uses the format kwarg of the view callable.

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
