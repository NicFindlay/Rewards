from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Glance, Profile
from .forms import SendGlance

# Create your views here.

def index(request):
    user_list = Profile.objects.order_by('user__first_name')

    context = {
        'user_list': user_list,
    }

    return render(request, 'Glancer/index.html', context)

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



