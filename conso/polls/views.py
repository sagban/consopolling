# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse, Http404
from .models import *
from django.template import loader
from django.urls import reverse
import re

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


def vote(request, team_id):

    questions = Question.objects.filter(team=team_id)
    team = Teams.objects.get(pk=team_id)
    if request.method == 'POST':

        if request.session.get(team_id, False):
            # Redisplay the question voting form.
            return render(request, 'team.html', {
                'questions': questions,
                'team': team,
                'error_message': "You've already voted! for team : " + team.team_name,
            })



        '''Validating Form server side'''
        for question in questions:
            que = question.question_id
            try:
                selected_choice = question.choice_set.get(choice_id=request.POST[str(que)])

            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(request, 'team.html', {
                    'questions': questions,
                    'team': team,
                    'error_message': "Plz, Vote all the given queries",
                })


        for question in questions:
            que = question.question_id
            selected_choice = question.choice_set.get(choice_id = request.POST[str(que)])
            '''Increase the counter Of the Vote'''
            selected_choice.votes += 1


            '''Saving the Choice'''
            selected_choice.save()
        request.session[team_id] = True
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
        return HttpResponseRedirect(reverse('review', args=(team_id)))
    #redirecting to the team page
    else:
        args = {
            'questions': questions,
            'team': team,
            'error_message': "There is Some Problem, Plz Vote Again",
        }
        return render(request, 'team.html', args)


def review(request, team_id):
    team = Teams.objects.get(pk=team_id)
    args ={
        "response" : "Thank you for voting team.",
        "team" : team,
    }

    return render(request, 'review.html', args)


def results(request):
    args={}
    return render(request, 'results.html', args)



def login_user(request):
    if request.session.get("conso", False):
        try:
            team = Teams.objects.all()
        except Teams.DoesNotExist:
            raise Http404("TEAMS does not exist")
        args = {'team': team,
                'error_message' : "You're already Logged in!",
                }
        return render(request, 'index.html', args)

    args = {}
    return render(request, 'login_user.html', args)


def login_validate(request):

    if request.method == "POST":

        if not re.match(r'^[6-9]\d{9}$',request.POST["mobile"]):
            args = {"error_message": "Plz, enter valid 10-digit mobile number"}
            return render(request, 'login_user.html', args)



        if request.POST["password"] == 'conso':
            try:
                team = Teams.objects.all()
            except Teams.DoesNotExist:
                raise Http404("TEAMS does not exist")
            request.session[request.POST["password"]] = True
            return render(request, 'index.html', {'team': team})

    args = {"error_message" : "Incorrect PassWord"}
    return render(request, 'login_user.html', args)