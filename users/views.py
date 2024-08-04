from django.shortcuts import render, redirect

from .forms import LoginForms, RegisterForms

#Authentication
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

#Login
def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            login_username = form['login_username'].value()
            password = form['password'].value()

        user = auth.authenticate(
            request,
            username=login_username,
            password=password
        )
        if user is not None:
            auth.login(request, user)
            return redirect('userOrders--page')
        else:
            return redirect('login')

    return render(request, 'login_page.html', {'form': form})

#logout 
def logout(request):
    auth.logout(request)
    return redirect('login')

    
#Register

def register(request):
    form = RegisterForms()

    if request.method == 'POST':
        form = RegisterForms(request.POST)

        if form.is_valid():
            username=form['username'].value()
            email=form['email'].value()
            password_1=form['password_1'].value()

            if User.objects.filter(username=username).exists():
                return redirect('register')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password_1,
            )
            user.save()
            return redirect('create__artists')

    return render(request, 'register.html', {'form': form})
