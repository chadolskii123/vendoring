from django.forms import ModelForm
from django import forms

from threadapp.models import Thread


class ThreadCreationForm(ModelForm):

    class Meta:
        model = Thread
        fields = ['thread_cd', 'thread_nm', 'content', 'image']
