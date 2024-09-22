
import os
import requests
from django.core.files.base import File
from io import BytesIO
from django.conf import settings
from django.core.files.storage import Storage

class BunnyCDNStorage(Storage):
    def __init__(self, location):
        self.location = location
        self.access_key = settings.BUNNY_PASSWORD

    def _save(self, name, content):
        # Definir a URL base do BunnyCDN para a localização (static ou media)
        if self.location == settings.STATICFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.STATICFILES_LOCATION}/"
        elif self.location == settings.MEDIAFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.MEDIAFILES_LOCATION}/"
        else:
            raise ValueError("Localização inválida para armazenamento")

        # Preservar a estrutura de diretórios
        relative_path = os.path.dirname(name)
        if relative_path:
            bunnycdn_url = os.path.join(bunnycdn_url, relative_path)

        # Concatena o nome do arquivo à URL
        file_name = os.path.basename(name)
        full_url = os.path.join(bunnycdn_url, file_name)

        # Cabeçalhos para autenticação e tipo de conteúdo
        headers = {
            "AccessKey": settings.BUNNY_PASSWORD,  # Certifique-se de usar a chave correta
            "Content-Type": "application/octet-stream",
        }

        # Realiza o upload do arquivo para o BunnyCDN
        with content as file_data:
            response = requests.put(full_url, headers=headers, data=file_data)

        # Verifica se o upload foi bem-sucedido
        if response.status_code in [201, 200]:
            return name  # Retorna o caminho relativo do arquivo
        else:
            raise Exception(f"Falha ao enviar o arquivo para o BunnyCDN: {response.status_code}")

    def _open(self, name, mode='rb'):
        """ Abre o arquivo do BunnyCDN e retorna um objeto File """
        if self.location == settings.STATICFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.STATICFILES_LOCATION}/{name}"
        elif self.location == settings.MEDIAFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.MEDIAFILES_LOCATION}/{name}"
        else:
            raise ValueError("Localização inválida para o arquivo")

        # Requisição para baixar o arquivo do BunnyCDN
        headers = {
            "AccessKey": self.access_key,
        }
        response = requests.get(bunnycdn_url, headers=headers)

        if response.status_code == 200:
            file_content = BytesIO(response.content)
            return File(file_content, name)
        else:
            raise Exception(f"Falha ao abrir o arquivo do BunnyCDN: {response.status_code}")

    def url(self, name):
        """ Retorna a URL pública do arquivo """
        if self.location == settings.STATICFILES_LOCATION:
            return f"{settings.STATIC_URL}{name}"
        elif self.location == settings.MEDIAFILES_LOCATION:
            return f"{settings.MEDIA_URL}{name}"
        else:
            raise ValueError("Localização inválida para URL")

    def exists(self, name):
        """ Checa se o arquivo já existe no BunnyCDN """
        return False  # Assumimos que o BunnyCDN cuida disso por nós

    def delete(self, name):
        """ Exclui o arquivo do BunnyCDN """
        if self.location == settings.STATICFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.STATICFILES_LOCATION}/{name}"
        elif self.location == settings.MEDIAFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.MEDIAFILES_LOCATION}/{name}"
        else:
            raise ValueError("Localização inválida para exclusão")

        headers = {
            "AccessKey": self.access_key,
        }
        response = requests.delete(bunnycdn_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Falha ao excluir o arquivo do BunnyCDN: {response.status_code}")

    def size(self, name):
        """Retorna o tamanho do arquivo armazenado no BunnyCDN."""
        if self.location == settings.STATICFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.STATICFILES_LOCATION}/{name}"
        elif self.location == settings.MEDIAFILES_LOCATION:
            bunnycdn_url = f"https://la.storage.bunnycdn.com/spot-storage/{settings.MEDIAFILES_LOCATION}/{name}"
        else:
            raise ValueError("Localização inválida para o arquivo")

        # Requisição para verificar o tamanho do arquivo
        headers = {
            "AccessKey": settings.BUNNY_PASSWORD,  # Usar o cabeçalho correto
        }
        response = requests.head(bunnycdn_url, headers=headers)  # Usamos 'HEAD' para obter os headers sem baixar o arquivo

        if response.status_code == 200:
            return int(response.headers.get('Content-Length', 0))
        else:
            raise Exception(f"Erro ao obter o tamanho do arquivo do BunnyCDN: {response.status_code}")

    
# Storage customizado para arquivos estáticos
class StaticStorage(BunnyCDNStorage):
    def __init__(self):
        super().__init__(settings.STATICFILES_LOCATION)

# Storage customizado para arquivos de mídia
class MediaStorage(BunnyCDNStorage):
    def __init__(self):
        super().__init__(settings.MEDIAFILES_LOCATION)