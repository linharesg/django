from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def current_user(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        return f"{user.first_name}"
    return False