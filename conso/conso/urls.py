"""conso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from polls import views

urlpatterns = [
    url(r'^$', views.login_user, name='login_user'),
    url(r'^login_validate/$', views.login_validate, name='login_validate'),
    url(r'^admin/', admin.site.urls),
    #main index page contains list of teams
    url(r'^teams/$', views.index, name='index'),
    #team/1
    url(r'^teams/(?P<team_id>[0-9]+)/$', views.team, name='team'),
    url(r'^teams/(?P<team_id>[0-9]+)/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /teams/5/results/
    url(r'^teams/results/$', views.results, name='results'),
    url(r'^teams/(?P<team_id>[0-9]+)/review/$', views.review, name='review'),
    # ex: /teams/5/vote/
    url(r'^teams/(?P<team_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
