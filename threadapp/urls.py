from django.urls import path

from threadapp.views import *

app_name = 'threadapp'

urlpatterns = [
    path('list/', ThreadListView.as_view(), name='library'),
    path('create/', ThreadCreateView.as_view(), name='create'),
    path('update/', thread_update, name='update'),
    path('detail/', thread_detail, name='detail'),
    path('thread_json/', thread_json, name='json'),
    path('save/', thread_save, name='save'),
    path('add/', thread_json, name='add'),
    # path('update/<int:pk>', ThreadUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>', ThreadDeleteView.as_view(), name='delete'),
    # path('qna/<int:pk>', ThreadListView.as_view(), name='qna'),

]
