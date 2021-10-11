from django.contrib import admin

# Register your models here.

from .models import Question

# In order to register a model as an interface to django admingg app,
# adming.site.register function can be used.
admin.site.register(Question)
