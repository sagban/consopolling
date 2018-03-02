# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from .models import *
from django.template import loader
#from django.core.context_processors import csrf


def index(request):
    try:
        team = Teams.objects.all()
    except Teams.DoesNotExist:
        raise Http404("TEAMS does not exist")
    return render(request, 'index.html', {'team': team})

def team(request, team_id):


    try:
        team = Teams.objects.get(pk=team_id)
    except Teams.DoesNotExist:
        raise Http404("Question does not exist")
    questions = Question.objects.filter(team=team_id).all()
    args = {
        'questions': questions,
        'team':team,
    }
    return render(request, 'team.html', args)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'details.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, team_id):
    questions = Question.objects.filter(team=team_id)
    for question in questions:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'team.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))