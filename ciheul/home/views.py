from django.conf import settings
from django.shortcuts import render

import os.path


def home(request):
    page = 'home' 
    return render(request, 
                  os.path.join(settings.DJANGO_ROOT,
                               'ciheul/home/templates/home/index.html'),
                  {'page': page})


def about(request):
    page = 'about'
    return render(request, 
                  os.path.join(settings.DJANGO_ROOT, 
                               'ciheul/home/templates/home/about-us.html'),
                  {'page': page})


def contact(request):
    page = 'contact'
    return render(request,
                  os.path.join(settings.DJANGO_ROOT,
                               'ciheul/home/templates/home/contact.html'),
                  {'page': page})


def jobs(request):
    page = 'jobs'
    return render(request,
                  os.path.join(settings.DJANGO_ROOT,
                               'ciheul/home/templates/home/jobs.html'),
                  {'page': page})

def team(request):
    return render(request, 
                  os.path.join(settings.DJANGO_ROOT,
                               '../home/templates/team.html'))


def services(request):
    return render(request, 
                  os.path.join(settings.DJANGO_ROOT, 
                               '../home/templates/services.html'))


def portfolio(request):
    return render(request, 
                  os.path.join(settings.DJANGO_ROOT,
                               '../home/templates/portfolio.html'))
