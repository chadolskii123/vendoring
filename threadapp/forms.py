from django.forms import ModelForm
from django import forms

from threadapp.models import Thread


class ThreadCreationForm(ModelForm):
    # owner = forms.MultipleChoiceField(queryset=Thread.objects.all(), required=False, label='회사')

    class Meta:
        model = Thread
        fields = ['thread_cd', 'thread_nm', 'content', 'image']
