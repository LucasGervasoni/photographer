# Create your views here.
from django.views.generic import TemplateView

class IndexView(TemplateView):
        template_name = "login_page.html"