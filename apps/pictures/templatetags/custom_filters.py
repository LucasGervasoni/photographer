from django import template
import os

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)

@register.filter(name='replace')
def replace(value, arg):
    """
    Substitui todas as ocorrências de uma substring por outra.
    O argumento deve ser passado como "substring_antiga,substring_nova".
    """
    old_value, new_value = arg.split(',')
    return value.replace(old_value, new_value)