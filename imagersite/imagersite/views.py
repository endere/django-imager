from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home_view(request):
    return render(
        request,
        'imagersite/home.html',
        context={}
    )


def profile_view(request):
    return render(
        request,
        'imagersite/profile.html',
        context={}
    )


def account_view(request):
    return render(request, 'registration/registration_form.html')
