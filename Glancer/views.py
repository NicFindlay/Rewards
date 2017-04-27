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

def find_current_user(request):
    for user in all_users:
        if user.user_id == request.user.id:
            print("XXXSSS")
            return user
    return None

def index(request):

    context = constructor(request)

    more_context = {

    }
    context.update(more_context)

    return render(request, 'Glancer/index.html', context)

def user(request, user_id):
    context = constructor(request)

    #Finding user object
    user_object = None
    for user in all_users:
        if str(user.user_id) == str(user_id):
            user_object = user

    glance_number = user_object.glance_number
    glance_giveaway = user_object.glance_giveaway

    glance_list = ['']
    glance_all = Glance.objects.all().order_by('date')
    for glance in glance_all:
        if(glance.receiver == user_object):
            glance_list.append(glance)

    more_context = {
        'user_object' : user_object,
        'glance_number' : glance_number,
        'glance_list' : glance_list,
        'glance_giveaway' : glance_giveaway,
    }
    context.update(more_context)

    return render(request, 'Glancer/user.html', context)



def send(request):
    context = constructor(request)
    current_user = find_current_user(request)  # find user who sent glance
    form = SendGlance()

    if current_user.glance_giveaway > 0:  #checking if user has glances to give away
        if request.method == 'POST':  #If submit has been clicked
            form = SendGlance(request.POST)
            if form.is_valid():
                for user in all_users:
                    if str(user.id) == str(request.POST.get('recipient')):
                            user.glance_number = user.glance_number + 1       #incrementing Total Glance number

                            current_user.glance_giveaway = current_user.glance_giveaway - 1   #decrementing Total Glance giveaway

                            user.save()                                         #Saving User Profile instance
                            create_glance(user, request.POST.get('description'))  #Instantiating new Glance

                return HttpResponseRedirect('/thanks/')  #Returning 'Thank You' page
    else:
        return HttpResponseRedirect('/limit/') #Add limit page

    more_context = {
        'user_list': all_users,
        'form': form,
    }
    context.update(more_context)

    return render(request, 'Glancer/send.html', context)


def thanks(request):

    context = constructor(request)

    more_context = {
        'user_list': all_users,
    }
    context.update(more_context)

    return render(request, 'Glancer/thanks.html', context )

def limit(request):

    context = constructor(request)

    more_context = {
        'user_list': all_users,
    }
    context.update(more_context)

    return render(request, 'Glancer/limit.html', context )


def glance_giveaway():
    return;

def create_glance(user, description):
    # NIC
    Receiver = user
    Description = description
    glance = Glance.create(date.today(), Description, Receiver)


def constructor(request):

    # Get username and check authenticity
    authentic = False
    username = None
    user_id = None
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id
        authentic = True

    context = {
        'user_list': all_users,
        'authentic': authentic,
        'username': username,
        'user_id': user_id,
    }
    return context;


