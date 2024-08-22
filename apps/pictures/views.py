
from wsgiref.util import FileWrapper
from django.db import transaction, OperationalError
from django.shortcuts import render, get_object_or_404, redirect
from apps.pictures.models import OrderImage, UserAction, OrderImageGroup, order_image_path
from apps.pictures.forms import OrderImageForm, PhotographerImageForm, OrderImageGroupForm
from apps.main_crud.models import Order

from django.views.generic import View, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.urls import reverse, reverse_lazy

from django.contrib import messages  # Import the messages module

import zipfile  # Import the zipfile module to create and manipulate ZIP files
import io  # Import the io module for handling byte streams
from django.http import HttpResponse, StreamingHttpResponse # Import HttpResponse to send HTTP responses
import os
from django.conf import settings
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
import time
from django.core.files.storage import default_storage

import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Download
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
                file_path = image.image.name

                if not default_storage.exists(file_path):
                    # Optionally log or handle the missing file case
                    print(f"File not found: {file_path}")
                    continue

                with default_storage.open(file_path, 'rb') as file_obj:
                    file_data = file_obj.read()
                    zip_file.writestr(os.path.basename(file_path), file_data)

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
        return render(request, 'uploadPage.html', {'order': order, 'form': form, 'group_form': group_form})

    @method_decorator(csrf_exempt)
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderImageForm(request.POST, request.FILES)
        group_form = OrderImageGroupForm(request.POST)

        if form.is_valid() and group_form.is_valid():
            image_group = OrderImageGroup.objects.filter(order=order).first()

            if not image_group:
                # Se não existir, crie um novo grupo
                image_group = group_form.save(commit=False)
                image_group.order = order
                image_group.save()
                

            images = []
            for index, f in enumerate(request.FILES.getlist('image')):
                
                order_image = OrderImage(
                    order=order,
                    image=f,
                    group=image_group,
                    photos_sent=form.cleaned_data.get('photos_sent'),
                    photos_returned=form.cleaned_data.get('photos_returned')
                )
                
                # Generate file path
                f.name = os.path.basename(order_image_path(instance=order_image, filename=f.name))
                
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
            
            return JsonResponse({'status': 'success', 'message': 'Images uploaded successfully.'})
        
        return JsonResponse({'status': 'error', 'message': 'Error uploading images. Please try again.'})

    
class PhotographerImageUploadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = PhotographerImageForm()
        group_form = OrderImageGroupForm()
        return render(request, 'uploadNewPhotos.html', {'form': form, 'group_form': group_form, 'order': order})
    
    @method_decorator(csrf_exempt)
    def post(self, request, pk):
            order = get_object_or_404(Order, pk=pk)
            form = PhotographerImageForm(request.POST, request.FILES)
            group_form = OrderImageGroupForm(request.POST)

            if form.is_valid() and group_form.is_valid():
                image_group = OrderImageGroup.objects.filter(order=order).first()

                if not image_group:
                    image_group = group_form.save(commit=False)
                    image_group.order = order
                    image_group.save()

                images = []
                for index, f in enumerate(request.FILES.getlist('image')):

                    order_image = OrderImage(
                        order=order,
                        image=f,
                        group=image_group
                    )
                    
                    # Generate file path
                    f.name = os.path.basename(order_image_path(instance=order_image, filename=f.name))
                    
                    order_image.save()

                    converted_image_url = order_image.convert_to_jpeg()
                    if converted_image_url:
                        order_image.save()

                    images.append(order_image)

                user_actions = [
                    UserAction(
                        user=request.user,
                        action_type='upload',
                        order=order,
                        order_image=image
                    ) for image in images
                ]
                UserAction.objects.bulk_create(user_actions)

                return JsonResponse({'status': 'success', 'message': 'Images uploaded successfully!'})

            return JsonResponse({'status': 'error', 'message': 'Error uploading images. Please try again.'})
        
        
# View to display all images related to an order
class OrderImageListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.all().order_by('uploaded_at') 
        paginator = Paginator(images, 20) 
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        image_count = images.count()
        return render(request, 'listImage.html', {'order': order, 'page_obj': page_obj, 'image_count': image_count})


#List Group of Files uploaded
class FilesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ['Admin'] 
    model = OrderImageGroup
    template_name = 'admin/listFiles.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

        # Get the search query
        search_query = self.request.GET.get('q', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        # Filter by search query
        if search_query:
            queryset = queryset.filter(
                Q(order__icontains=search_query) |
                Q(editor_note__icontains=search_query) |
                Q(services__icontains=search_query) |
                Q(scan_url__icontains=search_query)
            )

        # Filter by date range
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(created_at__date__gte=start_date_parsed)

        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(created_at__date__lte=end_date_parsed)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context
    
    
#Delete Files uploaded

class FileDeleteView(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
    group_required = ['Admin']
    login_url = reverse_lazy('login')
    model = OrderImageGroup
    template_name = 'admin/delete.html'
    success_url = reverse_lazy('list_files')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'File'
        return context
    
    
# List Log Actions

class LogListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ['Admin'] 
    model = UserAction
    template_name = 'admin/listLogs.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(action_type__icontains=search_query) |
                Q(order__order_number__icontains=search_query)
            )

        if start_date:
            start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
            queryset = queryset.filter(action_date__gte=start_date)

        if end_date:
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
            queryset = queryset.filter(action_date__lte=end_date)

        queryset = queryset.order_by('action_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context
    

#Delete Logs

class LogDeleteView(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
    group_required = ['Admin']
    login_url = reverse_lazy('login')
    model = UserAction
    template_name = 'admin/delete.html'
    success_url = reverse_lazy('list_logs')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Logs'
        return context
    
    