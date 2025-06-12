from django import template

register = template.Library()


@register.filter
def get_range(value):
    return range(1, value + 1)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
