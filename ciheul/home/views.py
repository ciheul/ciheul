from django.shortcuts import render
from django.conf import settings
import os.path


def home(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/index.html'))


def about(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/about-us.html'))


def team(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/team.html'))


def services(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/services.html'))


def portfolio(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/portfolio.html'))


def contact(request):
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/home/contact.html'))
