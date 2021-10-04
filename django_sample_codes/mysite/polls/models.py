from django.db import models

# Create your models here.

# A django model inherits from Model class held in django.db.models module.
# Each class variable in a model represents a database field.
# Each field is represnted by an instance of a Field class which tells django
# what datatype to use in database.
# The first positional optional argument for a Filed is used to give it a human
# readable name. If the name field isn't provided, django will use a machine
# readable name.
# Some fields have required arguments as well as optional arguments.
# A primary key is added to django models automatically. (can be overrided)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
