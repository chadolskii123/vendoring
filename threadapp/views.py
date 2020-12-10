from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from accountapp.forms import User
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
    context_object_name = 'object_list'

    template_name = 'snippets/list_table.html'

#    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        context['title'] = "Thread_list"
        context['cols'] = ['thead_cd', 'thread_nm', 'content']
        return context


class ThreadDetailView(DetailView):
    model = Thread
    context_object_name = 'target_thread'
    template_name = 'threadapp/detail.html'


def thread_json(request):
    search = request.GET.get('search', None)

    if search:
        lookups = Q(thread_nm__icontains=search) | Q(thread_cd__icontains=search)
        thread_all = Thread.objects.filter(lookups)
    else:
        thread_all = Thread.objects.all()

    offset = int(request.GET.get('offset', 1))  # 없으면 1로 지정
    limit = int(request.GET.get('limit', 10))

    data = []

    for thread in thread_all[offset:offset+limit]:

        inner_data = {
            "id": thread.thread_cd,
            "thread_nm": thread.thread_nm,
            "content": thread.content
        }
        data.append(inner_data)

    thread_count = thread_all.count()
    json_data = {
        "total": thread_count,
        "thread_count": thread_count,
        "rows": data
    }
    return JsonResponse(json_data, status=200)
