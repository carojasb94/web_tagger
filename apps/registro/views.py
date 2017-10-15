from django.shortcuts import render


def home(request):
    print("home request")
    print(request)
    return render(request, template_name='templates/home.html',
                  context={})


def do_login(request):
    print("do_login request")
    print(request)
    return render(request, template_name='templates/login.html',
                  context={})


def do_logout(request):
    print("do_logout request")
    print(request)
    pass



