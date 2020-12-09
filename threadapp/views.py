from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from threadapp.forms import ThreadCreationForm
from threadapp.models import Thread


class ThreadCreateView(CreateView):
    model = Thread
    form_class = ThreadCreationForm
    context_object_name = 'target_thread'
    template_name = 'threadapp/create.html'
    success_url = reverse_lazy('threadapp:list')


class ThreadListView(ListView):
    model = Thread
    context_object_name = 'thread_list'
    template_name = 'threadapp/list.html'

    # paginate_by = 10


class ThreadDetailView(DetailView):
    model = Thread
    context_object_name = 'target_thread'
    template_name = 'threadapp/detail.html'
