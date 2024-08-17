from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderImage, UserAction, OrderImageGroup
from .forms import OrderImageForm, PhotographerImageForm, OrderImageGroupForm
from main_crud.models import Order

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib import messages  # Import the messages module

import zipfile  # Import the zipfile module to create and manipulate ZIP files
import io  # Import the io module for handling byte streams
from django.http import HttpResponse  # Import HttpResponse to send HTTP responses
import os
from django.conf import settings

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
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for image in images:
                image_path = image.image.path
                relative_path = os.path.relpath(image_path, 'media')
                zip_file.write(image_path, relative_path)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="order_{order.address}_{order.pk}.zip"'
        return response

# Upload 

class OrderImageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderImageForm()
        group_form = OrderImageGroupForm()
        return render(request, 'uploadPage.html', {'form': form, 'group_form': group_form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        files = request.FILES.getlist('image')
        form = OrderImageForm(request.POST, request.FILES)
        group_form = OrderImageGroupForm(request.POST)

        if form.is_valid() and group_form.is_valid():
            image_group = group_form.save(commit=False)
            image_group.order = order
            image_group.save()

            images = []
            for index, f in enumerate(files):
                f.name = f'Spotlight{index + 1:02d}{f.name[f.name.rfind("."):]}'  # Ex: Spotlight01.jpg
                
                order_image = OrderImage(
                    order=order,
                    image=f,
                    group=image_group,
                    photos_sent=form.cleaned_data.get('photos_sent'),
                    photos_returned=form.cleaned_data.get('photos_returned')
                )
                order_image.save()
                
                # Convert the image if necessary
                converted_image_url = order_image.convert_to_jpeg()
                
                # Save the order image with the converted image
                if converted_image_url:
                    order_image.save()
                
                images.append(order_image)
            
            # Update order status
            order.order_status = 'Production'
            order.save()

            # Register user actions
            user_actions = [
                UserAction(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                ) for image in images
            ]
            UserAction.objects.bulk_create(user_actions)
            
            return redirect('order_images', pk=order.pk)
        
        messages.error(request, 'Error uploading images. Please try again.')
        return render(request, 'uploadPage.html', {'form': form, 'group_form': group_form, 'order': order})

class PhotographerImageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = PhotographerImageForm()
        group_form = OrderImageGroupForm()
        return render(request, 'uploadNewPhotos.html', {'form': form, 'group_form': group_form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        files = request.FILES.getlist('image')
        form = PhotographerImageForm(request.POST, request.FILES)
        group_form = OrderImageGroupForm(request.POST)
        
        if form.is_valid() and group_form.is_valid():
            image_group = group_form.save(commit=False)
            image_group.order = order
            image_group.save()

            images = []
            for index, f in enumerate(files):
                f.name = f'Spotlight{index + 1:02d}{f.name[f.name.rfind("."):]}'  # Ex: Spotlight01.jpg
                
                order_image = OrderImage(
                    order=order, 
                    image=f,
                    group=image_group  # Connect image to group
                )
                order_image.save()
                
                # Convert the image if necessary
                converted_image_url = order_image.convert_to_jpeg()
                
                # Save the order image with the converted image
                if converted_image_url:
                    order_image.save()
                
                images.append(order_image)
            
            # Log the upload actions
            user_actions = [
                UserAction(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                ) for image in images
            ]
            UserAction.objects.bulk_create(user_actions)
            
            return redirect('order_images', pk=order.pk)
        
        messages.error(request, 'Error uploading images. Please try again.')
        return render(request, 'uploadNewPhotos.html', {'form': form, 'group_form': group_form, 'order': order})


# View to display all images related to an order
class OrderImageListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.all()
        image_count = images.count()
        return render(request, 'listImage.html', {'order': order, 'images': images, 'image_count': image_count})
