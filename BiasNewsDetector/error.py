from django.contrib import messages
from django.http import HttpResponseRedirect


def error_handler(request, error):
    messages.error(request, error)
    request.path = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(request.path)
