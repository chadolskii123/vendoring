from django.contrib import messages
from django import forms
from django.utils.safestring import mark_safe

from vendori.utils import track_dhl


class DhlForm(forms.Form):
    awb_no = forms.CharField(max_length=120)

    class Meta:
        labels = {
            'aws_no': "AWB# "
        }

    def clean(self):
        request = self.request
        data = self.cleaned_data
        awb = self.cleaned_data.get["awb_no"]
        tracking_history = track_dhl(awb)
        if not tracking_history.exists():
            msg = "존재하지 않는 AWB# 입니다. 확인 후 다시 입력해주세요."
            messages.success(request, mark_safe(msg))
            raise forms.ValidationError("")
        self.tracking_history = tracking_history
        return data
