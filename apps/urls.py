# urls.py
from django.urls import path

from apps.bot.webhook import webhook
from apps.views import UserCreateView, GetMeView, RequestViewSet, get_message_count, get_all_messages, today_new, \
    unread_new_count

urlpatterns = [
    path('sign-up', UserCreateView.as_view(), name='user-create'),
    path('get-me', GetMeView.as_view(), name='get-me'),

    path('webhook', webhook, name='bot-webhook'),
    path('requests', RequestViewSet.as_view(), name='request'),
    path('message-count', get_message_count, name='message-count'),
    path('all-message', get_all_messages, name='all-message'),
    path('today_new', today_new, name='today-new'),
    path("unread-count/", unread_new_count, name="unread_count"),

]
