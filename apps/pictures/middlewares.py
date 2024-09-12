import logging
from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from django.contrib.auth import logout
import datetime

logger = logging.getLogger(__name__)

class LargeFileUploadMiddleware(MiddlewareMixin):
    """
    Middleware para gerenciar uploads grandes. Monitora o tamanho dos uploads e ajusta o tempo limite de upload.
    """
    MAX_UPLOAD_SIZE = 20 * 1024 * 1024 * 1024  # Limite de 20GB

    def process_request(self, request):
        if request.method == 'POST' and request.content_type.startswith('multipart/form-data'):
            content_length = int(request.META.get('CONTENT_LENGTH', 0))
            logger.debug(f"Upload iniciado com tamanho: {content_length} bytes")

            # Checks if the file size is above the defined limit
            if content_length > self.MAX_UPLOAD_SIZE:
                logger.warning(f"Upload de arquivo excede o limite permitido: {content_length} bytes")
                raise SuspiciousOperation("O arquivo enviado é muito grande.")

            # The timeout is no longer adjusted here, we trust the web server settings

    def process_exception(self, request, exception):
        if isinstance(exception, SuspiciousOperation):
            logger.error("Exceção levantada durante o upload de arquivo grande: SuspiciousOperation")
            return HttpResponseBadRequest("Arquivo grande demais para processar.")
        return None

    def process_response(self, request, response):
        # Adjust headers for large uploads if necessary
        if request.method == 'POST' and 'multipart/form-data' in request.content_type:
            response['X-Upload-Large-File'] = 'True'
        return response
    
    
class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        
        # Set the inactivity timeout
        timeout = getattr(settings, 'AUTO_LOGOUT_DELAY', 1800)  # 30 minutos
        
        # Get the timestamp of the last activity as a string
        last_activity_str = request.session.get('last_activity')
        
        if last_activity_str:
            # Convert string back to datetime
            last_activity = datetime.datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S.%f')
            elapsed_time = (datetime.datetime.now() - last_activity).total_seconds()
            if elapsed_time > timeout:
                logout(request)
                return
        
        # Update the timestamp of the last activity as a string
        request.session['last_activity'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        