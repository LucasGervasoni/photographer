from django.shortcuts import render, redirect

from apps.users.forms import LoginForms, RegisterForms
from apps.users.models import CustomUser
from django.contrib.auth import get_user_model
#Authentication
from django.contrib.auth.models import User
from django.contrib import auth

from django.views.generic import FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.db.models import Q

User = get_user_model()
# Create your views here.

#Login
def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            login_username = form.cleaned_data['login_username']
            password = form.cleaned_data['password']

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
class RegisterView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    group_required = ['Admin','Manager']
    login_url = reverse_lazy('login')
    form_class = RegisterForms
    template_name = 'user_form.html'
    success_url = reverse_lazy('listUsers')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password_1 = form.cleaned_data['password_1']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone_1 = form.cleaned_data['phone_1']
        phone_2 = form.cleaned_data['phone_2']
        address = form.cleaned_data['address']
        group = form.cleaned_data['group']

        if User.objects.filter(username=username).exists():
            return redirect('register')

        # Create the User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password_1,
            first_name=first_name,
            last_name=last_name,
            phone_1=phone_1,
            phone_2=phone_2,
            address=address
        )
        user.save()

        # Add user to the selected group
        group.user_set.add(user)
        
        if group.name == 'Manager' or group.name == 'Admin':
            user.is_superuser = True
            user.is_staff = True
            user.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New User'
        context['button'] = 'Create'
        return context

#List Users
class UserListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ['Admin','Manager'] 
    model = CustomUser
    template_name = 'listUsers.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = CustomUser.objects.all().order_by('username')
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone_1__icontains=query) |
                Q(phone_2__icontains=query) |
                Q(address__icontains=query)
            )
        return queryset


#Update

class UserUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ['Admin','Manager']
    login_url = reverse_lazy('login')
    model = CustomUser
    form_class = RegisterForms
    template_name = 'user_form.html'
    success_url = reverse_lazy('listUsers')
    
    def form_valid(self, form):
        user = form.instance
        password_1 = form.cleaned_data.get('password_1')
        password_2 = form.cleaned_data.get('password_2')

        if password_1 and password_2:
            if password_1 == password_2:
                user.set_password(password_1)
            else:
                form.add_error('password_2', 'Passwords do not match')
                return self.form_invalid(form)
        # Else, if no password provided, we don't change the existing password
        
        group = form.cleaned_data.get('group')
        if group:  # Se o grupo foi selecionado no formulário
            user.groups.clear()
            user.groups.add(group)

            # Verificar se o grupo é "Manager" e atribuir as permissões apropriadas
            if group.name == 'Manager' or group.name == 'Admin':
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False

        # Salvar as alterações do usuário
        user.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        context['button'] = 'Update'
        return context

#Delete

class UserDeleteView(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
    group_required = ['Admin','Manager']
    login_url = reverse_lazy('login')
    model = CustomUser
    template_name = 'deleteUser.html'
    success_url = reverse_lazy('listUsers')
    