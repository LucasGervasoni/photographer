from django.shortcuts import render
from .forms import ImageForm
from .models import Image

from django.views.generic.list import ListView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Create your views here.
def uploadPage(request):
 if request.method == "POST":
  form = ImageForm(request.POST, request.FILES)
  if form.is_valid():
   form.save()
 form = ImageForm()
 img = Image.objects.all()
 return render(request, 'uploadPage.html', {'img':img, 'form':form})

class ListImages(GroupRequiredMixin,LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        group_required = [u"Admin" u"EquipMember"]
        model = Image
        template_name = "listImage.html"