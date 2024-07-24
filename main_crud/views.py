from django.views.generic import TemplateView

class ServicesCreateArtists(TemplateView):
        template_name = "main_crud/admin/services__create--artists.html"
        
class ServicesCreateOrders(TemplateView):
        template_name = "main_crud/admin/services__create--orders.html"

class ServicesListArtists(TemplateView):
        template_name = "main_crud/admin/services__list--artists.html"
        
class ServicesListOrders(TemplateView):
        template_name = "main_crud/admin/services__list--orders.html"
class UserPageOrders(TemplateView):
        template_name = "main_crud/user/user__orders--page.html"