# Create your views here.
from django.views.generic import TemplateView

class ServicesView(TemplateView):
        template_name = "pages/admin/services.html"
        
class UserUploadPage(TemplateView):
        template_name = "pages/user-pages/user__upload--page.html"