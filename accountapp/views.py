from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, FormView, UpdateView

from accountapp.decorations import owner_check
from accountapp.forms import RegisterForm, LoginForm, User, AccountUpdateForm, PasswordUpdateForm
from accountapp.mixins import RequestFormAttachMixin, NextUrlMixin


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    """
    NextUrlMixin : 기존에 보던 페이지가 있으면 로그인 후에 다시 그 페이지로 갈 수 있도록 함
    RequsetFormAttachMixin : request에 담긴 값들을 넘겨줌
    *************************************************
        def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    *************************************************
    """
    form_class = LoginForm
    success_url = "/"
    template_name = "accountapp/login.html"
    default_next = "/"

    def form_valid(self, form):
        next_url = self.get_next_url()
        return redirect(next_url)


class AccountRegistView(CreateView):
    form_class = RegisterForm
    template_name = 'accountapp/register.html'

    def get_success_url(self):
        msg = f"가입이 완료되었습니다."
        messages.success(self.request, msg)
        return reverse("accountapp:login")


@method_decorator(owner_check, 'get')
@method_decorator(owner_check, 'post')
class AccountSettingView(UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = 'accountapp/update.html'

    def get_success_url(self):
        msg = f"수정 완료되었습니다."
        messages.success(self.request, msg)
        return reverse('accountapp:setting', kwargs={'pk': self.object.pk})


class PasswordSettingView(UpdateView):
    model = User
    form_class = PasswordUpdateForm
    template_name = 'accountapp/password.html'

    def get_success_url(self):
        msg = f"수정 완료되었습니다."
        messages.success(self.request, msg)
        return reverse('home')
