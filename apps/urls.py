# urls.py
from django.urls import path

from apps.bot.webhook import webhook
from apps.views import UserCreateView, GetMeView, RequestViewSet, GetMessagesCount, GetAllMessages, \
    TodayNewViewListAPIView, \
    UnreadNewCountListView

urlpatterns = [
    path('sign-up', UserCreateView.as_view(), name='user-create'),
    path('get-me', GetMeView.as_view(), name='get-me'),

    path('webhook', webhook, name='bot-webhook'),
    path('requests', RequestViewSet.as_view(), name='request'),
    path('message-count', GetMessagesCount.as_view(), name='message-count'),
    path('all-message', GetAllMessages.as_view(), name='all-message'),
    path('today_new', TodayNewViewListAPIView.as_view(), name='today-new'),
    path("unread-count", UnreadNewCountListView.as_view(), name="unread_count"),

]
