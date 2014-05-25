from ciheul.jendela24.models import UserProfile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseGone 
from django.shortcuts import redirect, render
from rauth import OAuth1Service
from requests.exceptions import ConnectionError
import json
import string
import random


consumer_key = 'UqOnzEFd328KDeMcbyEX1w'
consumer_secret = 'lMNt9lXX1FtrlaWNXPGWicZP8lql1HeRdBKcNCLiX8w'
        
twitter = OAuth1Service(
    name='twitter',    
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')

#ip_address = 'http://127.0.0.1:8002/jendela24'
ip_address = 'http://192.168.1.103/jendela24/'


def login_twitter(request):
    print "accounts.login_twitter"
    if login_session(request):
        print "login using session"
        #return HttpResponseRedirect('http://127.0.0.1:8002/accounts/profile')
        return HttpResponseRedirect(ip_address)
    
    try:
        # get request token and request token secret
        print "get request_token from twitter api..."
        request_token, request_token_secret = twitter.get_request_token()
        print 'request_token:', request_token
        print 'request_token_secret:', request_token_secret
    except ConnectionError:
        print "[ERROR] Max retries exceeded to Twitter API."
        return HttpResponseGone()

    request.session['request_token_secret'] = request_token_secret

    # get authorize url
    authorize_url = twitter.get_authorize_url(request_token)
    print 'authorize_url:', authorize_url
    
    return HttpResponse(authorize_url)
    #return HttpResponseRedirect(authorize_url)
    

def login_session(request):
    print "accounts.login_session"
    try:
        s = Session.objects.get(pk=request.COOKIES['sessionid'])
        user_info = s.get_decoded()
        return login_ciheul(request, user_info['username'], \
            user_info['password'])
    except ObjectDoesNotExist:
        print "session does not exist."
    except KeyError:
        print "no sessionid"
    return False


def redirect(request):
    print "accounts.redirect"
    # TODO check if request is coming from twitter. otherwise, malicious attack

    sessionid = request.COOKIES['sessionid']
    request_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']

    try:
        s = Session.objects.get(pk=sessionid).get_decoded()
        request_token_secret = s['request_token_secret']
    except ObjectDoesNotExist:
        print "session does not exist"
        return HttpResponse('Fail session.')

    print "get auth_session from twitter api..."
    twitter_session = twitter.get_auth_session( \
        request_token, request_token_secret, \
        method='POST', data={'oauth_verifier': oauth_verifier}) \

    r = twitter_session.get('statuses/user_timeline.json')
    u = json.loads(r.text)

    fullname = u[0]['user']['name']
    username = u[0]['user']['screen_name']
    description = u[0]['user']['description']
    location = u[0]['user']['location']
    homepage = u[0]['user']['url']
    if not homepage:
        homepage = ''
    profile_image_url = u[0]['user']['profile_image_url']

    try:
        # check if specified user exists in table auth.user
        user = User.objects.get(username=username)
        # TODO this is the worst way
        password = '!!rancakendal!!'
        user_profile = UserProfile.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        # TODO refactor to register() function
        first_name, last_name = split_fullname(fullname)
        password = '!!rancakendal!!'
        user = User.objects.create(username=username, \
            password=make_password(password), \
            first_name=first_name, last_name=last_name) 
        user_profile = UserProfile.objects.create(user=user, \
            location=location, description=description, homepage=homepage, \
            profile_image_url=profile_image_url)

    request.session['username'] = username
    request.session['password'] = password
    request.session['user_id'] = user_profile.id


    # TODO get from twitter_session
    #request.session['oauth_token'] = 
    #request.session['oauth_token_secret'] = 

    status = login_ciheul(request, username, password)
    if status:
        response = HttpResponseRedirect(ip_address)
        response.set_cookie('user_id', user_profile.id, max_age=1209600)
        return response
    return HttpResponse('Wrong password. Malicious attack? <a href="/accounts/login">login</a>')


def redirect_twitter(request):
    print "accounts.redirect_twitter"
    return HttpResponseRedirect('http://127.0.0.1:8002/accounts/profile')


def login_form(request):
    print "accounts.login_form"
    if request.user.is_authenticated():
        return HttpResponseRedirect('http://127.0.0.1:8002/accounts/profile')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if login_ciheul(request, username, password):
        return HttpResponseRedirect(request.GET.get('next', '/accounts/profile'))
    return render(request, 'registration/login.html')


def login_ciheul(request, username, password):
    print "accounts.login_ciheul"
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return True
    return False


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(ip_address)


def register(request):
    return HttpResponse('register')


@login_required
def profile(request):
    print "profile"
    return HttpResponse('hi, ' + request.session['username']) 


@login_required
def settings(request):
    return HttpResponse('settings. <a href="/accounts/logout">logout</a>')


def split_fullname(fullname):
    tokens = fullname.split(' ')
    firstname = ' '.join(tokens[0:-1])
    lastname = tokens[-1]
    return firstname, lastname


def generate_random_password(size=20):
    # TODO generate more secure random password
    chars = string.letters + string.digits + string.punctuation
    random_password = ''
    for i in range(size):
        random_password += random.choice(chars)
    # increase stronger security using pkbdf2_sha256
    return random_password
