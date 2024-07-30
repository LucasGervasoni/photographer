# Create your views here.
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

#Services Page
class ServicesView(GroupRequiredMixin,LoginRequiredMixin,TemplateView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        template_name = "baseAdmin.html"