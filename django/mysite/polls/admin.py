from django.contrib import admin

# Register your models here.

from .models import Question, Choice
# In order to register a model as an interface to django admingg app,
# adming.site.register function can be used.
# Customizations could be done through defining a class.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}),
                 ('Data information', {'fields': ['pub_date'],
                                       'classes': ['collaps']})]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
