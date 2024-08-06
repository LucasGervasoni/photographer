from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderImage
from .forms import OrderImageForm
from main_crud.models import Order

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class OrderImageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderImageForm()
        return render(request, 'uploadPage.html', {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        files = request.FILES.getlist('image')
        form = OrderImageForm(request.POST, request.FILES)
        if form.is_valid():
            for f in files:
                OrderImage.objects.create(order=order, image=f)
            return redirect('order_images', pk=order.pk)
        return render(request, 'uploadPage.html', {'form': form, 'order': order})

# View to display all images related to an order
class OrderImageListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.all()
        return render(request, 'listImage.html', {'order': order, 'images': images})