from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Glance, Profile
from .forms import SendGlance
from django.contrib.auth.views import login, logout

# Create your views here.

def check_authentication(request, *args, **kwargs):
    user_flag = login(request, *args, *kwargs)
    return user_flag


def index(request):
    user_list = Profile.objects.order_by('user__first_name')

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
        print(username)


    context = {
        'user_list': user_list,
        'authentic' : authentic,
        'username' : username,
        'user_id' : user_id,
    }

    return render(request, 'Glancer/index.html', context)

def user(request):

    user_flag = True
    print(user_flag)
    return render(request, 'Glancer/index.html')

def send(request):

    user_list = Profile.objects.order_by('user__first_name')

    form = SendGlance()


    if request.method == 'POST':
        form = SendGlance(request.POST)
        if form.is_valid():
            print(request.POST.get('recipient'))
            print(request.POST.get('description'))
            return HttpResponseRedirect('/thanks/')


    context = {
        'user_list': user_list,
        'form': form,
    }

    return render(request, 'Glancer/send.html', context)

def thanks(request):


    context = {

    }
    return render(request, 'Glancer/thanks.html', context )








