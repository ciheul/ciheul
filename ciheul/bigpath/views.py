# Create your views here.
from django.shortcuts import render

def home(request):
    # hack: though in 'settings.py' IP_ADDR has been assigned as 'localhost'
    # import process keeps changing IP_ADDR to '127.0.0.1'
    IP_ADDRESS = '127.0.0.1'
    PORT = '8000'
    params = {
        'title_head': 'BigPath - Location Tracer',
        'title': 'BigPath',
        'ip_addr': IP_ADDRESS,
        'port': PORT,
    }
    return render(request, "base_bigpath.html", params)
