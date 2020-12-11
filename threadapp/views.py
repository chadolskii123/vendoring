import copy

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin, UpdateView

from accountapp.forms import User
from threadapp.forms import ThreadCreationForm
from threadapp.models import Thread


class ThreadCreateView(CreateView):
    model = Thread
    form_class = ThreadCreationForm
    context_object_name = 'target_thread'
    template_name = 'threadapp/list.html'
    success_url = reverse_lazy('threadapp:library')


def thread_update(request):
    thread_cd = request.GET.get('thread_cd')
    thread = get_object_or_404(Thread, thread_cd=thread_cd)
    form = ThreadCreationForm(request.POST or None, instance=thread)
    if form.is_valid():
        form.save()

        return redirect('window.close()')
    context = {
        'form': form,
        'thread_cd': thread_cd
    }
    return render(request, 'threadapp/update.html', context)


class ThreadListView(ListView, FormMixin):
    model = Thread
    context_object_name = 'object_list'
    form_class = ThreadCreationForm

    template_name = 'snippets/list_table.html'

    #    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        context['title'] = "Thread_list"
        context['col1'] = 'thread_cd'
        context['col2'] = 'thread_nm'
        context['col3'] = 'content'
        context['col4'] = 'image'

        context['create_form'] = self.form_class
        return context


def thread_detail(request):
    thread_cd = request.GET.get('thread_cd')
    thread_obj = Thread.objects.get(thread_cd=thread_cd)
    context = {
        'target_obj': thread_obj
    }
    return render(request, 'threadapp/detail.html', context)


def thread_json(request):
    search = request.GET.get('search', None)
    sort = request.GET.get('sort', None)
    order = request.GET.get('order', None)
    offset = int(request.GET.get('offset', None))
    limit = int(request.GET.get('limit', None))

    thread_all = Thread.objects.all()

    if search:
        lookups = Q(thread_nm__icontains=search) | Q(thread_cd__icontains=search)
        thread_all = thread_all.filter(lookups)
    else:
        thread_all = thread_all

    data = []
    thread_list = thread_all.order_by('-created_at')

    if sort and order == 'asc':
        thread_list = thread_list.order_by(f'{sort}')
        thread_list = thread_list[offset:offset + limit]
    elif sort and order == 'desc':
        thread_list = thread_list.order_by(f'-{sort}')
        thread_list = thread_list[offset:offset + limit]
    else:
        thread_list = thread_list[offset:offset + limit]

    for thread in thread_list:
        inner_data = {
            "thread_cd": thread.thread_cd,
            "thread_nm": thread.thread_nm,
            "content": thread.content,
        }
        data.append(inner_data)

    thread_count = thread_all.count()
    json_data = {
        "total": thread_count,
        "thread_count": thread_count,
        "rows": data,
    }

    return JsonResponse(json_data)


def thread_save(request):
    rm_list = request.POST.get('rm_list')
    rm_cd = rm_list.split(',')
    thread_obj = Thread.objects.filter(thread_cd__in=rm_cd)
    rs = thread_obj.delete()

    json_data = {
        "msg": rs
    }
    return JsonResponse(json_data)
