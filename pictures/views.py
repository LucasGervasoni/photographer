from .models import File


from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class UploadList(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = File
        template_name = "listImage.html"
        
        #Return the orders by user
        def get_queryset(self):
                
                if self.request.user.is_superuser:       
                        self.object_list = File.objects.all()
                else:
                        self.object_list = File.objects.filter(author=self.request.user)
                
                return  self.object_list
