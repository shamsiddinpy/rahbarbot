# urls.py
from django.urls import path
from apps.views import UserCreateView, GetMeView

urlpatterns = [
    path('sign-up', UserCreateView.as_view(), name='user-create'),
    path('get-me', GetMeView.as_view(), name='get-me'),

]
