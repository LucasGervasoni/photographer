# Create your views here.
from django.views.generic import TemplateView

class LoginView(TemplateView):
        template_name = "login_page.html"

class ServicesView(TemplateView):
        template_name = "admin/services.html"
        
class ServicesCreateArtists(TemplateView):
        template_name = "admin/services__create--artists.html"

class ServicesCreateOrders(TemplateView):
        template_name = "admin/services__create--orders.html"

class ServicesListArtists(TemplateView):
        template_name = "admin/services__list--artists.html"

class ServicesListOrders(TemplateView):
        template_name = "admin/services__list--orders.html"

class UserPageOrders(TemplateView):
        template_name = "user-pages/user__orders--page.html"
        
class UserUploadPage(TemplateView):
        template_name = "user-pages/user__upload--page.html"