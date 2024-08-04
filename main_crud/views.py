# from django.db.models.query import QuerySet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Order
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

#List Orders for user
class UserPageOrders(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Order
        template_name = "main_crud/user/UserOrdersList.html"
        
        #Return the orders by user
        def get_queryset(self):
                
                if self.request.user.is_superuser:       
                        self.object_list = Order.objects.all()
                else:
                        self.object_list = Order.objects.filter(user=self.request.user)
                
                return  self.object_list
