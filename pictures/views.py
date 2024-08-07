from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderImage, UserAction
from .forms import OrderImageForm, PhotographerImageForm
from main_crud.models import Order

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib import messages  # Import the messages module

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
        
        # Log the download action
        UserAction.objects.create(
            user=request.user,
            action_type='download',
            order=order
        )

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

# Upload with Editor note
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
                image = OrderImage.objects.create(order=order, image=f, editor_note=form.cleaned_data.get('editor_note', ''))
                # Log the download action
                UserAction.objects.create(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                )
                messages.success(request, 'Images uploaded successfully!')
            return redirect('order_images', pk=order.pk)
        messages.error(request, 'Error uploading images. Please try again.')
        return render(request, 'uploadPage.html', {'form': form, 'order': order})

# Upload just new photos
class PhotographerImageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = PhotographerImageForm()
        return render(request, 'uploadNewPhotos.html', {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        files = request.FILES.getlist('image')
        form = PhotographerImageForm(request.POST, request.FILES)
        if form.is_valid():
            for f in files:
                image = OrderImage.objects.create(order=order, image=f)
                UserAction.objects.create(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                )
                messages.success(request, 'Images uploaded successfully!')
            return redirect('order_images', pk=order.pk)
        messages.error(request, 'Error uploading images. Please try again.')
        return render(request, 'uploadNewPhotos.html', {'form': form, 'order': order})

# View to display all images related to an order
class OrderImageListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.all()
        return render(request, 'listImage.html', {'order': order, 'images': images})
    