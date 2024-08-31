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

            # Verifica se o tamanho do arquivo está acima do limite definido
            if content_length > self.MAX_UPLOAD_SIZE:
                logger.warning(f"Upload de arquivo excede o limite permitido: {content_length} bytes")
                raise SuspiciousOperation("O arquivo enviado é muito grande.")

            # O timeout não é mais ajustado aqui, confiamos nas configurações do servidor web

    def process_exception(self, request, exception):
        if isinstance(exception, SuspiciousOperation):
            logger.error("Exceção levantada durante o upload de arquivo grande: SuspiciousOperation")
            return HttpResponseBadRequest("Arquivo grande demais para processar.")
        return None

    def process_response(self, request, response):
        # Ajusta os cabeçalhos para uploads grandes, se necessário
        if request.method == 'POST' and 'multipart/form-data' in request.content_type:
            response['X-Upload-Large-File'] = 'True'
        return response
    
    
class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        
        # Define o tempo limite de inatividade
        timeout = getattr(settings, 'AUTO_LOGOUT_DELAY', 1800)  # 30 minutos
        
        # Obtém o timestamp da última atividade como string
        last_activity_str = request.session.get('last_activity')
        
        if last_activity_str:
            # Converte a string de volta para datetime
            last_activity = datetime.datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S.%f')
            elapsed_time = (datetime.datetime.now() - last_activity).total_seconds()
            if elapsed_time > timeout:
                logout(request)
                return
        
        # Atualiza o timestamp da última atividade como string
        request.session['last_activity'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')