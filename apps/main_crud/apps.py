from django.apps import AppConfig


class MainCrudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main_crud'
    verbose_name = 'Orders Dashboard'
