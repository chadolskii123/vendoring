from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import FormView

from vendori.forms import DhlForm
from vendori.utils import track_dhl


def home_view(request):
    context = {
        'title': '메인 - Vendori'
    }
    return render(request, 'index.html', context)


class CheckDhlView(FormView):
    form_class = DhlForm
    success_url = '/dhl/tracking_list.html'
    template_name = "dhl/track.html"

    def get(self, request, **kwargs):
        request = self.request
        awb = request.GET.get("awb_no")
        if awb:
            tracking_history = track_dhl(awb)
            if tracking_history:
                context = {"object_list": tracking_history}
                return render(request, 'dhl/tracking_list.html', context)
            else:
                msg = "존재하지 않는 AWB# 입니다. 확인 후 다시 입력해주세요."
                messages.success(request, mark_safe(msg))
                context = {"form": self.get_form()}
                return render(request, 'dhl/track.html', context)
        else:
            context = {"form": self.get_form()}
            return render(request, 'dhl/track.html', context)
