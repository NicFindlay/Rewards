from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Glance, Profile
from django.contrib.auth.models import User
from .forms import SendGlance
from django.contrib.auth.views import login, logout
from datetime import date

all_users = Profile.objects.order_by('user__first_name')
# Create your views here.

def check_authentication(request, *args, **kwargs):
    user_flag = login(request, *args, *kwargs)
    return user_flag


def index(request):

    user_list = all_users

    #Check if user authenticated
    authentic = False
    if request.user.is_authenticated():
        authentic = True

    #Get username
    username = None
    user_id = None
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id

    print(user_id)

    context = {
        'user_list': user_list,
        'authentic' : authentic,
        'username' : username,
        'user_id' : user_id,
    }

    return render(request, 'Glancer/index.html', context)

def user(request, user_id):

    # Get username
    username = None
    if request.user.is_authenticated():
        username = request.user.username

    #Finding user object
    user_object = None
    user_list = all_users
    for user in user_list:
        if str(user.user_id) == str(user_id):
            user_object = user

    glance_number = user_object.glance_number
    glance_giveaway = user_object.glance_giveaway

    glance_list = ['']
    glance_all = Glance.objects.all().order_by('date')
    for glance in glance_all:
        if(glance.receiver == user_object):
            glance_list.append(glance)

    context = {
        'user_id' : user_id,
        'username' : username,
        'user_object' : user_object,
        'glance_number' : glance_number,
        'glance_list' : glance_list,
        'glance_giveaway' : glance_giveaway
    }
    return render(request, 'Glancer/user.html', context)



def send(request):

    user_list = all_users
    # Get username
    username = None
    user_id = None
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id

    form = SendGlance()

    if request.method == 'POST':
        form = SendGlance(request.POST)
        if form.is_valid():
            for user in user_list:
                if str(user.id) == str(request.POST.get('recipient')):
                        user.glance_number = user.glance_number + 1       #incrementing Total Glance number
                        user.save()                                         #Saving User Profile instance
                        create_glance(user, request.POST.get('description'))  #Instantiating new Glance

            return HttpResponseRedirect('/thanks/')  #Returning 'Thank You' page

    context = {
        'user_list': user_list,
        'form': form,
        'user_id' : user_id,
    }
    return render(request, 'Glancer/send.html', context)


def thanks(request):

    # Get username
    username = None
    user_id = None
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id

    context = {
        'user_list': all_users,
        'user_id' : user_id
    }
    return render(request, 'Glancer/thanks.html', context )


def glance_giveaway():
    return;

def create_glance(user, description):
    # NIC
    Receiver = user
    Description = description
    glance = Glance.create(date.today(), Description, Receiver)














