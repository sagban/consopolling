# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse, Http404
from .models import *
from django.template import loader
from django.urls import reverse

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

def results(request, team_id):
    response = "You're looking at the results of team %s. You provided"
    return HttpResponse(response % team_id)

def vote(request, team_id):

    questions = Question.objects.filter(team=team_id)
    team = Teams.objects.get(pk=team_id)
    if request.method == 'POST':

        for question in questions:
            que = question.question_id
            try:
                selected_choice = question.choice_set.get(choice_id = request.POST[str(que)])

            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(request, 'team.html', {
                    'questions': questions,
                    'team': team,
                    'error_message': "Plz, Vote all the given queries",
                })
            else:
                selected_choice.votes += 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(team_id)))
    else:
        args = {
            'questions': questions,
            'team': team,
        }
        return render(request, 'team.html', args)