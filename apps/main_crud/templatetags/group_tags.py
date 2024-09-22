from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
  if user.is_authenticated:
    return user.groups.filter(name=group_name).exists()
  return False

@register.filter
def format_services(services):
    return ', '.join(services.strip('[]').replace("'", "").split(', '))
  
  
@register.filter(name='replace')
def replace(value, arg):
    """
    Substitui todas as ocorrências de uma substring por outra.
    O argumento deve ser passado como "substring_antiga,substring_nova".
    """
    old_value, new_value = arg.split(',')
    return value.replace(old_value, new_value)