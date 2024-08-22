import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)

class LargeFileUploadMiddleware(MiddlewareMixin):
    MAX_UPLOAD_SIZE = 20 * 1024 * 1024 * 1024  # Limite de 20GB
    MAX_UPLOAD_TIME = 300  # 300 segundos (5 minutos) para timeout de upload

    def process_request(self, request):
        if request.method == 'POST' and request.content_type.startswith('multipart/form-data'):
            content_length = int(request.META.get('CONTENT_LENGTH', 0))
            if content_length > self.MAX_UPLOAD_SIZE:
                logger.warning(f"Upload de arquivo excede o limite permitido: {content_length} bytes")
                raise SuspiciousOperation("O arquivo enviado é muito grande.")

            if content_length > 0:
                # Adiciona o tempo limite adaptativo para o upload
                timeout = max(self.MAX_UPLOAD_TIME, content_length / (1024 * 1024))
                request.META['wsgi.input'].settimeout(timeout)

                # Log dos uploads grandes
                if content_length > 500 * 1024 * 1024:  # Loga arquivos maiores que 500MB
                    logger.info(f"Upload de grande arquivo: {content_length / (1024 * 1024)} MB")

    def process_exception(self, request, exception):
        if isinstance(exception, SuspiciousOperation):
            return HttpResponseBadRequest("Arquivo grande demais para processar.")
        return None

    def process_response(self, request, response):
        # Verifica se a resposta é de upload de arquivo grande e ajusta os cabeçalhos conforme necessário
        if request.method == 'POST' and 'multipart/form-data' in request.content_type:
            response['X-Upload-Large-File'] = 'True'
        return response
