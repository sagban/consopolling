# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

class Teams(models.Model):
    team_id = models.AutoField(primary_key=True, null=False)
    team_name = models.TextField(max_length=200, null=False )
    team_detail = models.TextField(max_length=4000, null=True)

    def __str__(self):
        return self.team_name


class Question(models.Model):
    question_id = models.AutoField(primary_key=True, default=0)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True, default = 0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text