from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

# format_suffix_patterns can be used to apply optional formatting options to
# the endpoints, it uses the format kwarg of the view callable.

urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(),
         name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHightlight.as_view(),
         name='snippet-highlight'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detial')
]

urlpatterns = format_suffix_patterns(urlpatterns)
