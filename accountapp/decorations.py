from django.http import HttpResponseForbidden

from accountapp.forms import User


def owner_check(func):
    def decorated(request, *args, **kwargs):
        print("GET BEFORE")
        user = User.objects.get(pk=kwargs['pk'])
        print(user)
        print("GET AFTER")
        if not user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
