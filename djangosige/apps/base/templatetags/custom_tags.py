from django import template
from django.forms import CheckboxInput

register = template.Library()

# Custom tag para verificar se field é checkbox


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__
