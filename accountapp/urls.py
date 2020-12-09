from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from accountapp.views import AccountRegistView, LoginView, AccountSettingView, PasswordSettingView

app_name = 'accountapp'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', AccountRegistView.as_view(), name='regist'),
    path('setting/<int:pk>', AccountSettingView.as_view(), name='setting'),
    path('password/<int:pk>', PasswordSettingView.as_view(), name='password')

]
