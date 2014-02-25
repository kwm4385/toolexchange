from django import template

register = template.Library()

""" template tag which allows queryset filtering. Usage:
      {% query books author=author as mybooks %}
      {% for book in mybooks %}
        ...
      {% endfor %}
"""
@register.assignment_tag
def query(qs, **kwargs):
    return qs.filter(**kwargs)
