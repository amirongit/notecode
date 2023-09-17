from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
