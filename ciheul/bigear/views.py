from django.shortcuts import render
#from settings import IP_ADDRESS, PORT


def home(request):
    # hack: though in 'settings.py' IP_ADDR has been assigned as 'localhost'
    # import process keeps changing IP_ADDR to '127.0.0.1'
    IP_ADDRESS = '127.0.0.1'
    PORT = '8000'
    return render(request, "base.html", {'ip_addr': IP_ADDRESS, 'port': PORT})
