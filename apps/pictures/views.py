
import threading
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
import boto3
import tarfile
from django.contrib.auth.models import Group
from botocore.config import Config
import logging

from setup import settings


logger = logging.getLogger(__name__)

# Create your views here.

# Download


class OrderImageDownloadView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        folder = request.GET.get('folder', 'default')

        if folder == 'edited':
            # Filtra imagens da pasta "Edited"
            images = order.image.filter(image__icontains='/Edited/', selected_for_exclusion=False)
        else:
            # Comportamento padrão
            images = order.image.filter(selected_for_exclusion=False)

        # Registra a ação de download
        UserAction.objects.create(
            user=request.user,
            action_type='download',
            order=order
        )

        address_safe = slugify(order.address)
        zip_filename = f'order_{address_safe}.zip'

        response = StreamingHttpResponse(
            self.stream_zip_file_from_bunny(images),
            content_type='application/zip'
        )
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        response['Content-Transfer-Encoding'] = 'binary'

        return response

    def stream_zip_file_from_bunny(self, images):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for image in images:
                file_name = image.image.name  # Caminho do arquivo no BunnyCDN

                print(f"Verificando arquivo: {file_name}")  # Depuração 1: Verificar nome do arquivo

                # Verifica se o arquivo existe no BunnyCDN antes de fazer o download
                if not self.check_file_exists_in_bunnycdn(file_name):
                    print(f"Arquivo não encontrado no BunnyCDN: {file_name}")  # Depuração 2: Arquivo não encontrado
                    continue

                # Baixa o arquivo do BunnyCDN e o adiciona ao zip
                file_content = self.download_file_from_bunnycdn(file_name)
                if file_content:
                    print(f"Arquivo baixado com sucesso: {file_name}")  # Depuração 3: Arquivo baixado com sucesso
                    print(f"Tamanho do arquivo baixado: {len(file_content)} bytes")  # Depuração 4: Ver tamanho do arquivo

                    relative_path = self.get_relative_path(file_name)
                    unique_name = self.get_unique_filename(zip_file, relative_path)
                    zip_file.writestr(unique_name, file_content)
                else:
                    print(f"Erro ao baixar o arquivo: {file_name}")  # Depuração 5: Erro ao baixar arquivo

        buffer.seek(0)
        print(f"Tamanho do buffer do ZIP: {buffer.getbuffer().nbytes} bytes")  # Depuração 6: Ver tamanho do ZIP gerado
        while chunk := buffer.read(1024):
            yield chunk

    def get_relative_path(self, file_path):
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

    def normalize_path(self, path):
        """Normaliza o caminho para evitar barras duplas."""
        return path.replace('//', '/').strip()

    def download_file_from_bunnycdn(self, file_name):
        """Baixa o arquivo diretamente do BunnyCDN."""
        url = self.ensure_valid_bunnycdn_url(file_name)


        headers = {
            "AccessKey": settings.BUNNY_PASSWORD
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.content  # Retorna o conteúdo do arquivo
            else:
                print(f"Erro ao baixar o arquivo {file_name} do BunnyCDN: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    def check_file_exists_in_bunnycdn(self, file_name):
        """Verifica se o arquivo existe no BunnyCDN."""
        url = self.ensure_valid_bunnycdn_url(file_name)

        headers = {
            "AccessKey": settings.BUNNY_PASSWORD
        }

        try:
            response = requests.head(url, headers=headers)
            return response.status_code == 200  # Retorna True se o arquivo existir
        except requests.exceptions.RequestException as e:
            print(f"Erro ao verificar existência do arquivo: {e}")
            return False
        
    def ensure_valid_url(self, url):
        """Adiciona o esquema 'https://' à URL, caso ela não tenha."""
        if not url.startswith('https://'):
            return 'https://' + url
        return url

    def ensure_valid_bunnycdn_url(self, file_name):
        """Gera a URL correta para o BunnyCDN, incluindo o caminho de mídia necessário."""
        base_url = settings.BUNNY_CDN_URL  # Assumindo que essa é a URL base, como 'https://spot-storage.b-cdn.net/'
        file_name = self.normalize_path(file_name)  # Normaliza o caminho

        # Certifique-se de que o caminho tenha dois "media"
        if not file_name.startswith('media/media'):
            file_name = f"media/media/{file_name.lstrip('media/')}"
        
        # Constrói a URL final
        url = f"{base_url}/{file_name}"

        # Certifica que a URL sempre tenha 'https://'
        return self.ensure_valid_url(url)


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

        form = OrderImageForm(request.POST, request.FILES, is_3d_scan_only=is_3d_scan_only)

        if form.is_valid() and group_form.is_valid():
            image_group = OrderImageGroup.objects.filter(order=order, created_by_view='OrderImageUploadView').first()

            if not image_group:
                image_group = group_form.save(commit=False)
                image_group.order = order
                image_group.created_by_view = 'OrderImageUploadView'
                image_group.save()

            images = []
            for f in request.FILES.getlist('image'):
                try:
                    relative_path = request.POST.get('relative_path', '')

                    order_image = OrderImage(
                        order=order,
                        image=f,
                        group=image_group,
                        photos_sent=form.cleaned_data.get('photos_sent'),
                        photos_returned=form.cleaned_data.get('photos_returned')
                    )

                    order_image.save()

                    # Conversão em thread separada
                    thread = threading.Thread(target=self.convert_image_in_background, args=(order_image,))
                    thread.start()

                    images.append(order_image)

                except Exception as e:
                    print(f"Error during file upload and processing: {e}")
                    return JsonResponse({'status': 'error', 'message': f"Error processing image: {e}"})

            scan_url = request.POST.get('scan_url')
            if is_3d_scan_only and scan_url:
                order.scan_url = scan_url
                order.save()

                UserAction.objects.create(
                    user=request.user,
                    action_type='3d scan',
                    order=order,
                )

            order.order_status = 'Uploaded'
            order.save()

            user_actions = [
                UserAction(
                    user=request.user,
                    action_type='upload',
                    order=order,
                    order_image=image
                ) for image in images
            ]
            UserAction.objects.bulk_create(user_actions)

            # Inicia a criação do ZIP de forma assíncrona
            thread = threading.Thread(target=self.create_zip_in_background, args=(image_group,))
            thread.start()

            return JsonResponse({'status': 'success', 'message': 'Images and/or 3D scan uploaded successfully.'})
        
        return JsonResponse({'status': 'error', 'message': 'Error uploading files. Please try again.'})

    def convert_image_in_background(self, order_image):
        """
        Função para realizar a compressão e conversão da imagem em um thread separado.
        """
        try:
            order_image.compress_and_convert()
        except Exception as e:
            print(f"Error during image conversion in background: {e}")

    def create_zip_in_background(self, image_group):
        """
        Função para criar o arquivo ZIP dos uploads sem filtrar imagens com base em pastas.
        """
        try:
            # Cria um buffer em memória para o ZIP
            zip_buffer = io.BytesIO()
            zip_filename = f"{slugify(image_group.order.address)}.zip"  # Nome do arquivo ZIP sem incluir o folder

            # Obtenha todas as imagens relacionadas ao grupo
            images = image_group.images.filter(selected_for_exclusion=False)

            # Cria o arquivo ZIP no buffer
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for image in images:
                    image_url = self.ensure_valid_bunnycdn_url(image.image.url)  # Adiciona o esquema correto à URL
                    file_content = self.download_file_from_bunnycdn(image_url)  # Faz o download do arquivo
                    if file_content:
                        file_name = os.path.basename(image_url)  # Obtém o nome do arquivo
                        zip_file.writestr(file_name, file_content)  # Adiciona o conteúdo do arquivo ao ZIP
                    else:
                        print(f"Erro ao baixar o arquivo da URL: {image_url}")

            # Move o cursor para o início do buffer
            zip_buffer.seek(0)

            # Faz o upload do ZIP para o BunnyCDN
            self.upload_zip_to_bunny(zip_buffer, zip_filename)

            # Atualiza o caminho no modelo OrderImageGroup
            bunny_url = f"{settings.BUNNY_CDN_URL}/media/zips/{zip_filename}"
            image_group.zip_file_path = bunny_url
            image_group.save()

            print(f"ZIP criado e enviado com sucesso para {bunny_url}")

        except Exception as e:
            print(f"Error during ZIP creation or upload: {e}")

            
    def ensure_valid_bunnycdn_url(self, url):
            """
            Adiciona o esquema 'https://' à URL, caso ela não tenha.
            """
            if not url.startswith('http://') and not url.startswith('https://'):
                return f"https://{url.lstrip('/')}"
            return url

    def download_file_from_bunnycdn(self, file_url):
            """
            Faz o download de um arquivo a partir do BunnyCDN usando a URL.
            """
            try:
                headers = {
                    "AccessKey": settings.BUNNY_PASSWORD
                }
                response = requests.get(file_url, headers=headers)
                if response.status_code == 200:
                    return response.content  # Retorna o conteúdo do arquivo
                else:
                    print(f"Erro ao baixar o arquivo {file_url} do BunnyCDN: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Erro durante o download do arquivo: {e}")
                return None
            
    def upload_zip_to_bunny(self, zip_buffer, zip_filename):
        """
        Função para fazer upload do ZIP para o BunnyCDN na zona de armazenamento.
        """
        try:
            # URL de upload correta na zona de armazenamento do BunnyCDN
            upload_url = f"https://la.storage.bunnycdn.com/spot-storage/media/zips/{zip_filename}"

            # Certifica-se de que a URL de upload tenha o esquema correto
            upload_url = self.ensure_valid_bunnycdn_url(upload_url)

            # Cabeçalhos de autenticação para o BunnyCDN
            headers = {
                "AccessKey": settings.BUNNY_PASSWORD  # Certifique-se de que sua chave de acesso esteja correta
            }

            # Faz o upload do arquivo para o BunnyCDN
            response = requests.put(upload_url, data=zip_buffer.getvalue(), headers=headers)

            if response.status_code in [200, 201]:
                print(f"Arquivo {zip_filename} enviado com sucesso para o BunnyCDN.")
            else:
                print(f"Erro ao enviar o arquivo {zip_filename} para o BunnyCDN: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erro durante o upload para o BunnyCDN: {e}")


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

            # Check if the user is in the Editor group
            is_editor = request.user.groups.filter(name='Editor').exists()
            if is_editor:
                relative_path = 'Edited/' + relative_path if relative_path else 'Edited'

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

                # Conversão em thread separada
                thread = threading.Thread(target=self.convert_image_in_background, args=(order_image,))
                thread.start()

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
    
    def convert_image_in_background(self, order_image):
        """
        Função para realizar a compressão e conversão da imagem em um thread separado.
        """
        order_image.compress_and_convert()



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

        # Verifica se o filtro para exibir apenas as fotos do Editor foi ativado
        filter_by_editor = request.GET.get('filter', '') == 'editor'

        if filter_by_editor:
            # Obtém o grupo "Editor"
            editor_group = Group.objects.get(name='Editor')

            # Filtra os usuários do grupo Editor que fizeram uploads
            editor_user_ids = editor_group.user_set.values_list('id', flat=True)

            # Obtém as imagens que foram enviadas pelos editores
            user_actions = UserAction.objects.filter(
                user_id__in=editor_user_ids,
                action_type='upload',  # Assumindo que 'upload' é registrado no campo action_type
                order=order
            ).values_list('order_image_id', flat=True)  # Obtém os IDs das imagens enviadas pelos editores

            # Filtrar as imagens relacionadas às ações dos editores
            images = order.image.filter(id__in=user_actions).order_by('uploaded_at')
        else:
            # Caso o filtro não esteja ativado, exibe todas as imagens do pedido
            images = order.image.all().order_by('uploaded_at')

        # Convertendo as imagens ou vídeos para miniaturas
        for image in images:
            if not image.converted_image:  # Verifica se a miniatura já existe
                image.convert_media()

        paginator = Paginator(images, 21)  # Paginação com 21 imagens por página
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
    
    