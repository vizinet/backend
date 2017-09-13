from django import template
register = template.Library()

@register.filter
def custom_index(List, i):
    return List[int(i)]
