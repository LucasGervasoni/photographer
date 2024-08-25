from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Support(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = "supportPage.html"

    def get(self, request, *args, **kwargs):
        # Add any context or logic here if needed
        return render(request, self.template_name)