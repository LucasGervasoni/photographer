
import uuid
from django.shortcuts import render, get_object_or_404, redirect
import requests
from apps.pictures.models import OrderImage, UserAction, OrderImageGroup, order_image_path
from apps.pictures.forms import OrderImageForm, PhotographerImageForm, OrderImageGroupForm
from apps.main_crud.models import Order
from django.views.generic import View, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.urls import reverse, reverse_lazy
import zipfile  # Import the zipfile module to create and manipulate ZIP files
import io  # Import the io module for handling byte streams
from django.http import FileResponse, HttpResponse, StreamingHttpResponse # Import HttpResponse to send HTTP responses
import os
from django.db.models import Q
from django.db.models import OuterRef, Subquery 
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import logging


logger = logging.getLogger(__name__)

# Create your views here.

# Download

class OrderImageDownloadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.filter(selected_for_exclusion=False)

        # Log the download action
        UserAction.objects.create(
            user=request.user,
            action_type='download',
            order=order
        )

        address_safe = slugify(order.address)
        zip_filename = f'order_{address_safe}.zip'

        response = StreamingHttpResponse(
            self.stream_zip_file(images),
            content_type='application/zip'
        )
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        response['Content-Transfer-Encoding'] = 'binary'

        return response

    def stream_zip_file(self, images):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for image in images:
                file_path = image.image.name

                if not default_storage.exists(file_path):
                    continue

                # Add the file and its relative path to the zip file
                with default_storage.open(file_path, 'rb') as file_obj:
                    relative_path = self.get_relative_path(file_path)
                    unique_name = self.get_unique_filename(zip_file, relative_path)
                    zip_file.writestr(unique_name, file_obj.read())

        buffer.seek(0)
        while chunk := buffer.read(8192):
            yield chunk

    def get_relative_path(self, file_path):
        # Remove the leading part of the path to get a relative path for the ZIP
        base_dir = 'media/'
        if file_path.startswith(base_dir):
            return file_path[len(base_dir):]
        return file_path

    def get_unique_filename(self, zip_file, filename):
        counter = 1
        unique_name = filename
        while unique_name in zip_file.namelist():
            name, ext = os.path.splitext(filename)
            unique_name = f"{name}_{counter}{ext}"
            counter += 1
        return unique_name
  
    
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
        group_form = OrderImageGroupForm(request.POST)

        services = request.POST.getlist('services')
        is_3d_scan_only = len(services) == 1 and '3d scan' in services

        # Passa o parâmetro is_3d_scan_only ao formulário para ajustar a validação
        form = OrderImageForm(request.POST, request.FILES, is_3d_scan_only=is_3d_scan_only)

        if form.is_valid() and group_form.is_valid():
            image_group = OrderImageGroup.objects.filter(order=order, created_by_view='OrderImageUploadView').first()

            if not image_group:
                image_group = group_form.save(commit=False)
                image_group.order = order
                image_group.created_by_view = 'OrderImageUploadView'
                image_group.save()

            images = []
            for index, f in enumerate(request.FILES.getlist('image')):
                relative_path = request.POST.get('relative_path', '')

                order_image = OrderImage(
                    order=order,
                    image=f,
                    group=image_group,
                    photos_sent=form.cleaned_data.get('photos_sent'),
                    photos_returned=form.cleaned_data.get('photos_returned')
                )

                file_path = order_image_path(instance=order_image, filename=f.name, relative_path=relative_path)
                f.name = os.path.basename(file_path)
                
                order_image.save()

                converted_image_url = order_image.convert_to_jpeg()
                if converted_image_url:
                    order_image.save()

                images.append(order_image)

            scan_url = request.POST.get('scan_url')
            if is_3d_scan_only and scan_url:
                order.scan_url = scan_url
                order.save()

                # Cria uma UserAction específica para o upload do 3D Scan
                UserAction.objects.create(
                    user=request.user,
                    action_type='3d scan',
                    order=order,
                )

            # Atualiza o status do pedido
            order.order_status = 'Uploaded'
            order.save()

            # Cria ações de usuário para cada imagem enviada
            user_actions = [
                UserAction(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                ) for image in images
            ]
            UserAction.objects.bulk_create(user_actions)

            return JsonResponse({'status': 'success', 'message': 'Images and/or 3D scan uploaded successfully.'})
        
        return JsonResponse({'status': 'error', 'message': 'Error uploading files. Please try again.'})


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
        group_form = OrderImageGroupForm(request.POST)
        services = request.POST.getlist('services')

        # Passing the selected services to the form
        form = PhotographerImageForm(request.POST, request.FILES, services=services)

        if form.is_valid() and group_form.is_valid():
            selected_services = group_form.cleaned_data.get('services', [])
            scan_url = group_form.cleaned_data.get('scan_url')

            # Check if only the 3D scan service was selected
            if '3d scan' in selected_services and len(selected_services) == 1:
                image_group = group_form.save(commit=False)
                image_group.order = order
                image_group.created_by_view = 'PhotographerImageUploadView'
                image_group.scan_url = scan_url  # Ensures that the 3D scan URL is saved

                image_group.save()

                # Register the 3D scan upload action
                UserAction.objects.create(
                    user=request.user,
                    action_type='3d Scan',
                    order=order,
                    order_image=None  # No images, only 3D scan
                )

                return JsonResponse({'status': 'success', 'message': '3D scan URL uploaded successfully!'})

            # If it is not just 3D scan, continue with the logic for file uploads
            last_image_group = OrderImageGroup.objects.filter(order=order, created_by_view='PhotographerImageUploadView').last()

            if last_image_group and request.session.get('current_file_list', []):
                image_group = last_image_group
            else:
                group_count = OrderImageGroup.objects.filter(order=order, created_by_view='PhotographerImageUploadView').count() + 1
                if group_count > 2:
                    group_count -= 1

                group_form.instance.group_name = f"PhotographerGroup{group_count}"
                image_group = group_form.save(commit=False)
                image_group.order = order
                image_group.created_by_view = 'PhotographerImageUploadView'
                image_group.scan_url = scan_url  # Ensures that the 3D scan URL is saved

                image_group.save()

                request.session['current_file_list'] = []

            file_list = request.session['current_file_list']
            images = []
            relative_path = request.POST.get('relative_path', '')

            for f in request.FILES.getlist('image'):
                file_list.append(f.name)

                order_image = OrderImage(
                    order=order,
                    image=f,
                    group=image_group
                )

                file_path = order_image_path(instance=order_image, filename=f.name, relative_path=relative_path)
                f.name = os.path.basename(file_path)

                order_image.save()

                converted_image_url = order_image.convert_to_jpeg()
                if converted_image_url:
                    order_image.save()

                images.append(order_image)

            request.session['current_file_list'] = file_list

            user_actions = [
                UserAction(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                ) for image in images
            ]
            UserAction.objects.bulk_create(user_actions)

            return JsonResponse({'status': 'success', 'message': 'Images uploaded successfully!', 'files': file_list})

        return JsonResponse({'status': 'error', 'message': 'Error uploading images. Please try again.'})



class CreateOrderImageGroupView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        # Check if there is already a recent unused group of images
        last_image_group = OrderImageGroup.objects.filter(order=order, created_by_view='PhotographerImageUploadView').last()

        if last_image_group and not OrderImage.objects.filter(group=last_image_group).exists():
            # If the last group of images has no associated images, reuse it
            return JsonResponse({'status': 'success', 'group_id': last_image_group.id})

        # Otherwise, create a new image group
        image_group = OrderImageGroup.objects.create(
            order=order,
            created_by_view='PhotographerImageUploadView'
        )

        return JsonResponse({'status': 'success', 'group_id': image_group.id})



# View to display all images related to an order
class OrderImageListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        images = order.image.all().order_by('uploaded_at') 
        
        # Converting images or videos to thumbnails
        for image in images:
            if not image.converted_image:  # Check if the thumbnail already exists
                image.convert_media()

        paginator = Paginator(images, 21) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        image_count = images.count()
        
        recent_scan = order.orderimagegroup_set.order_by('-created_at').first()
        scan_url = recent_scan.scan_url if recent_scan else None
        
        return render(request, 'listImage.html', {
            'order': order, 
            'page_obj': page_obj, 
            'image_count': image_count,
            'scan_url': scan_url  
        })


class ToggleImageSelectionView(View):
    def post(self, request, image_id):
        selected = request.POST.get('selected') == 'true'
        image = get_object_or_404(OrderImage, id=image_id)
        
        # Atualizar a flag selected_for_exclusion
        image.selected_for_exclusion = selected
        image.save()

        return JsonResponse({'status': 'success', 'selected': image.selected_for_exclusion})


#List Group of Files uploaded
class FilesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ['Admin','Manager'] 
    model = OrderImageGroup
    template_name = 'admin/listFiles.html'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

        # Get the search query
        search_query = self.request.GET.get('q', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        # Filter by search query
        if search_query:
            queryset = queryset.filter(
                Q(order__address__icontains=search_query) |  # Assuming 'address' is a field in the Order model
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
    group_required = ['Admin','Manager']
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
    group_required = ['Admin','Manager'] 
    model = UserAction
    template_name = 'admin/listLogs.html'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        user_filter = self.request.GET.get('user', '')

        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(action_type__icontains=search_query) |
                Q(order__address__icontains=search_query)
            )

        if start_date:
            start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
            queryset = queryset.filter(action_date__gte=start_date)

        if end_date:
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
            queryset = queryset.filter(action_date__lte=end_date)
        
        if user_filter:
            queryset = queryset.filter(user__id=user_filter)

        queryset = queryset.order_by('-action_date')

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        user_filter = self.request.GET.get('user', '')
        context['selected_user'] = int(user_filter) if user_filter.isdigit() else None
        context['users'] = get_user_model().objects.all()
        return context
    

#Delete Logs

class LogDeleteView(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
    group_required = ['Admin','Manager']
    login_url = reverse_lazy('login')
    model = UserAction
    template_name = 'admin/delete.html'
    success_url = reverse_lazy('list_logs')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Logs'
        return context
    
    