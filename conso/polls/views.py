# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from .models import *
from django.template import loader
#from django.core.context_processors import csrf


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    args = {
        'latest_question_list': latest_question_list,
    }

    return render(request, 'index.html', args)



def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'details.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)