from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:  # More specific exception handling
        group = Group.objects.create(name=group_name) # This line will create the group if it doesn't exist.
    return True if group in user.groups.all() else False