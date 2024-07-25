from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.list import ListView
from .models import CreateOrders
from django.urls import reverse_lazy
        
class ServicesCreateOrders(CreateView):
        model = CreateOrders
        fields = ["date", "time", "addressOne", "AddressTwo", "ZipCode", "city", "state", "services"]
        template_name = "main_crud/admin/services__create--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesUpdateOrders(UpdateView):
        model = CreateOrders
        fields = ["date", "time", "addressOne", "AddressTwo", "ZipCode", "city", "state", "services"]
        template_name = "main_crud/admin/services__create--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesDeleteOrders(DeleteView):
        model = CreateOrders
        template_name = "main_crud/admin/services__delete--orders.html"
        success_url = reverse_lazy('list__orders')
        
class ServicesListOrders(ListView):
        model = CreateOrders
        template_name = "main_crud/admin/services__list--orders.html"
        
class UserPageOrders(ListView):
        model = CreateOrders
        template_name = "main_crud/user/user__orders--page.html"

class ServicesListArtists(TemplateView):
        template_name = "main_crud/admin/services__list--artists.html"
        