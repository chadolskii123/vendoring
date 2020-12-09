from django.http import HttpResponseForbidden

from accountapp.forms import User
from threadapp.models import Thread


def owner_check(func):
    def decorated(request, *args, **kwargs):
        thread = Thread.objects.get(pk=kwargs['pk'])
        if not thread.owner == request.user.company_cd:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
