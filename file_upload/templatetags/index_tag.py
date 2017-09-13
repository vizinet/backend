from django import template
register = template.Library()

@register.filter
def index_tag(List, i):
    return List[int(i)]
