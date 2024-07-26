# from django.db.models.query import QuerySet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Orders
from users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

#Orders
class ServicesCreateOrders(GroupRequiredMixin,LoginRequiredMixin,CreateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        fields = ["user", "date", "time", "addressOne", "addressTwo", "zipCode", "city", "state", "services"]
        template_name = "main_crud/admin/services__create--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesUpdateOrders(GroupRequiredMixin,LoginRequiredMixin,UpdateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        fields = ["user", "date", "time", "addressOne", "addressTwo", "zipCode", "city", "state", "services"]
        template_name = "main_crud/admin/services__create--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesDeleteOrders(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        template_name = "main_crud/admin/services__delete--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesListOrders(GroupRequiredMixin,LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        template_name = "main_crud/admin/services__list--orders.html"
        
class UserPageOrders(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Orders
        template_name = "main_crud/user/user__orders--page.html"
        
        def get_queryset(self):
                self.object_list = Orders.objects.filter(user=self.request.user)
                
                return  self.object_list
        
#Artists
class ServicesDeleteOrders(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        template_name = "main_crud/admin/services__delete--orders.html"
        success_url = reverse_lazy('list__artists')

class ServicesListArtists(GroupRequiredMixin,LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        template_name = "main_crud/admin/services__list--artists.html"
