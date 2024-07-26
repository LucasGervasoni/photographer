from django.shortcuts import render, redirect
from .forms import LoginForms, RegisterForms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

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
            messages.success(request, f'{login_username} successfully logged in!')
            return redirect('user__orders--page')
        else:
            messages.error(request, 'Error when logging in')
            return redirect('login')

    return render(request, 'login_page.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successful!')
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
                messages.error(request, 'User already exist')
                return redirect('register')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password_1,
            )
            user.save()
            messages.success(request, 'Registration successfully Complete!')
            return redirect('login')

    return render(request, 'register.html', {'form': form})

class ServicesCreateArtists(GroupRequiredMixin,LoginRequiredMixin,CreateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        fields = ["username", "firstName", "lastName", "phoneOne", "phoneTwo", "addressOne", "addressTwo", "zipCode", "city", "state"]
        template_name = "services__create--artists.html"
        success_url = reverse_lazy('list__artists')
        
class ProfileUpdate(GroupRequiredMixin,LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u"Admin" u"EquipMember"]
    template_name = "services__create--artists.html"
    model = Profile
    fields = ["username", "firstName", "lastName", "phoneOne", "phoneTwo", "addressOne", "addressTwo", "zipCode", "city", "state"]
    success_url = reverse_lazy("list__artists")

