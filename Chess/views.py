from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.template.loader import render_to_string
import datetime
from .models import User
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from .tasks import  *
from time import sleep


# Create your views here.


def set_online_status(user,status):
    cache.set(user.username,status,300)



def index(request):
    c={}

    if request.user.is_authenticated():
        c['user'] = True
        set_online_status(request.user,'Online')
    return HttpResponse(render_to_string('index.html', c))




def registration(request):
    c = {}
    validation = {}
    validation.update(csrf(request))
    c = RequestContext(request, validation)
    if request.user.is_authenticated():
        c['user'] = True
        set_online_status(request.user,'Online')
        if request.user.is_superuser:
            c['admin']=True
    return HttpResponse(render_to_string('registration.html',c))

def createuser(request):
    c = {}
    validation={}
    validation.update(csrf(request))
    c = RequestContext(request, validation)
    if request.user.is_authenticated():
        c['user'] = True
        set_online_status(request.user,'Online')
    if request.method == 'POST':
        username = request.POST['display_name']
        password = request.POST['password']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        conf_pass=request.POST['password_confirmation']
        email=request.POST['email']
        try:
            user = User.objects.get(username=username)
            if user is not None:
                c['main_error'] = True
                c['Error']='This user already exists'
                return HttpResponse(render_to_string('registration.html', c))
        except BaseException:
            if conf_pass != password:
                c['main_error'] = True
                c['Error'] = 'Passwords are different'
                return HttpResponse(render_to_string('registration.html', c))
            c.update(csrf(request))
            new_user = User.objects.create_user(username=username,email = email, password=password, first_name=first_name, last_name=last_name)
            new_user.save



            return redirect('/registration')
    return redirect('/registration')

def login_page(request):
    c = {}
    validation = {}
    validation.update(csrf(request))
    c = RequestContext(request, validation)
    if request.user.is_authenticated():
        c['user'] = True
        set_online_status(request.user,'Online')
    return HttpResponse(render_to_string('login.html', c))



def log(request):
    c={}
    validation = {}
    validation.update(csrf(request))
    c = RequestContext(request, validation)
    if request.user.is_authenticated():
        set_online_status(request.user,'Online')
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        try:
            user_model=User.objects.get(username=username)
            if not user_model.is_active:
                c['main_error'] = True
                c['Error'] = 'This user is not active'
                return HttpResponse(render_to_string('registration.html', c))
            user = authenticate(username=username, password=password)
            c['main_error']=False
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                c['main_error'] = True
                c['Error'] = 'This user does not exist'
                return HttpResponse(render_to_string('registration.html', c))

        except BaseException:
            c['main_error'] = True
            c['Error'] = 'This user does not exist'
            return HttpResponse(render_to_string('registration.html', c))

def logout_view(request):
    if request.user.is_authenticated():
        set_online_status(request.user,'Offline')
    logout(request)
    return redirect('/')


def profile_view(request):
    if request.user.is_authenticated():
        c = {}
        validation = {}
        validation.update(csrf(request))
        c = RequestContext(request, validation)

        if request.user.is_authenticated():
            c['user'] = True
            c["user_profile"]=request.user
            c['games']=request.user.defeats+request.user.victorys
            set_online_status(request.user, 'Online')
        if(cache.get(request.user.username)=='Online'):
            c['status']=True
        return HttpResponse(render_to_string('user_page.html', c))
    return redirect('/login')




def searching_game(user):
    if not cache.get("search_lock"):
        cache.set("search_lock",True)
        player = {'id': user.id, 'rating': user.rating}
        if not cache.get('players'):
            players = []
            players.append(player)
            players_in_game=cache.get("players_in_game")
            if players_in_game:
                if player not in players_in_game:
                    players = []
                    players.append(player)
                    print(cache.set('players', players))
            else:
                players = []
                players.append(player)
                print(cache.set('players', players))

        else:
            players = cache.get('players')
            if not player in players:
                if cache.get('players_in_game') and (not player in cache.get('players_in_game')):
                    players.append(player)
                elif not cache.get('players_in_game'):
                    players.append(player)
                    print(cache.set('players', players))
        cache.set("search_lock", False)
    else: searching_game(user)





@never_cache
def board(request):
    c = {}

    if request.user.is_authenticated():
        c['user'] = True
        c["user_profile"]=request.user
        set_online_status(request.user, 'Online')
        searching_game(request.user)
        #create_games.delay()
        return HttpResponse(render_to_string('board.html', c))
    return redirect('/login')




