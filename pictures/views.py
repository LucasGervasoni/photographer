from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderImage
from .forms import OrderImageForm
from main_crud.models import Order

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

import zipfile  # Import the zipfile module to create and manipulate ZIP files
import io  # Import the io module for handling byte streams
from django.http import HttpResponse  # Import HttpResponse to send HTTP responses

import os

# Create your views here.
class OrderImageDownloadView(LoginRequiredMixin, View): 
    login_url = reverse_lazy('login') 

    def get(self, request, pk): 
        order = get_object_or_404(Order, pk=pk)  
        images = order.image.all() 

        # Create a zip file in memory
        buffer = io.BytesIO()  # Create an in-memory byte-stream buffer to store the ZIP file
        with zipfile.ZipFile(buffer, 'w') as zip_file:  # Create a ZipFile object, opening it for writing ('w')
            for image in images:  # Iterate over all images related to the order
                image_path = image.image.path  # Get the file system path of the image
                zip_file.write(image_path, os.path.basename(image_path))  # Add the image to the ZIP file, using its basename as the file name in the ZIP

        buffer.seek(0)  # Rewind the buffer to the beginning
        response = HttpResponse(buffer, content_type='application/zip')  # Create an HTTP response with the ZIP file content
        response['Content-Disposition'] = f'attachment; filename="order_{pk}_images.zip"'  # Set the Content-Disposition header to indicate a file attachment with a specified filename
        return response  # Return the HTTP response

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