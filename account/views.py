from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import AppUser
from app.models import App
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # appUser = AppUser.objects.filter(user=request.user)
    appUser = get_object_or_404(AppUser, user=request.user)
    print(appUser.username)
    appList =  App.objects.filter(user=request.user).order_by('-created')
    return render(request, 'account/home.html', {'appUser':appUser, 'appList':appList})

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('account:home')
        else:
            return render(request, 'account/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'account/login.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password'] != None:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'account/signup.html', {'error':'username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                newUser = AppUser()
                newUser.username = request.POST['pick_name']
                newUser.email = request.POST['username']
                auth.login(request, user)
                newUser.user = request.user
                newUser.save()
                return redirect('account:home')
        else:
            return render(request, 'account/signup.html', {'error':'Passwords must match'})
    else:
        return render(request, 'account/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('account:login')


def about(request):
    return render(request, 'account/about.html')
