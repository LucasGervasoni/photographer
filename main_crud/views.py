# from django.db.models.query import QuerySet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Orders
from .forms import OrderForm
from users.models import Profile
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

#Create Orders
class ServicesCreateOrders(GroupRequiredMixin,LoginRequiredMixin,CreateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        form = OrderForm
        template_name = "main_crud/admin/createOrders.html"
        success_url = reverse_lazy('listOrders')

#Update Orders 
class ServicesUpdateOrders(GroupRequiredMixin,LoginRequiredMixin,UpdateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        form_class = OrderForm
        template_name = "main_crud/admin/createOrders.html"
        success_url = reverse_lazy('listOrders')

#Delete Orders
class ServicesDeleteOrders(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        template_name = "main_crud/admin/delete.html"
        success_url = reverse_lazy('listOrders')
        
        def get_context_data(self, *args, **kwargs):
                context = super().get_context_data(*args, **kwargs)

                context['title'] = "Orders"

                return context

#List Orders  
class ServicesListOrders(GroupRequiredMixin,LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Orders
        template_name = "main_crud/admin/listOrders.html"

#List Orders for user
class UserPageOrders(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Orders
        template_name = "main_crud/user/UserOrdersList.html"
        
        #Return the orders by user
        def get_queryset(self):
                self.object_list = Orders.objects.filter(user=self.request.user)
                
                return  self.object_list

#Artists
   
#Delete Artists
class ServicesDeleteArtists(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        template_name = "main_crud/admin/delete.html"
        success_url = reverse_lazy('listArtists')
        
        def get_context_data(self, *args, **kwargs):
                context = super().get_context_data(*args, **kwargs)

                context['title'] = "Artists"

                return context

#List Artists
class ServicesListArtists(GroupRequiredMixin,LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Profile
        template_name = "main_crud/admin/listArtists.html"
