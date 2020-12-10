from django.urls import path

from threadapp.views import ThreadListView, ThreadCreateView, ThreadDetailView, thread_json

app_name = 'threadapp'

urlpatterns =[
    path('list/', ThreadListView.as_view(), name='list'),
    path('create/', ThreadCreateView.as_view(), name='create'),
    path('detail/<int:pk>', ThreadDetailView.as_view(), name='detail'),
    path('thread_json/', thread_json, name='json'),
    # path('update/<int:pk>', ThreadUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>', ThreadDeleteView.as_view(), name='delete'),
    # path('qna/<int:pk>', ThreadListView.as_view(), name='qna'),

]