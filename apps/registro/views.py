
from django.shortcuts import render


def home(request):
    print("home request")
    return render(request, template_name='home.html',
                  context={})


def do_login(request):
    print("do_login request")
    return render(request, template_name='login.html',
                  context={})


def do_logout(request):
    print("do_logout request")
    pass



