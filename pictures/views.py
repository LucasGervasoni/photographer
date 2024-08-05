from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Image

from django.http import HttpResponse
from django.template import loader

from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
def uploadPage(request):
  form = ImageForm(request.POST, request.FILES)
  if request.method == "POST":
    images = request.FILES.getlist('photo')
    for image in images:
          image_ins = Image(photo = image)
          image_ins.save()
          
    return redirect('uploadLists')
  
  context = {'form': form} 
  return render(request, 'uploadPage.html', context)

class UploadList(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Image
        template_name = "listImage.html"
        
        #Return the orders by user
        def get_queryset(self):
                
                if self.request.user.is_superuser:       
                        self.object_list = Image.objects.all()
                else:
                        self.object_list = Image.objects.filter(user=self.request.user)
                
                return  self.object_list
