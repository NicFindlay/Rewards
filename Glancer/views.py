from django.shortcuts import render
from django.http import HttpResponse
from .models import Glance, Profile

# Create your views here.

def index(request):
    user_list = Profile.objects.order_by('user__first_name')

    context = {
        'user_list': user_list,
    }

    return render(request, 'Glancer/index.html', context)



