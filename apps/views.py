from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Request
from apps.serializer import UserSerializer, RequestSerializer


@extend_schema(tags=['Authentication'])
class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'telegram_id'

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": access_token,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User"])
class GetMeView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class RequestViewSet(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetMessagesCount(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.all()

    def get(self, request, *args, **kwargs):
        count = Request.objects.count()
        return Response({"count": count})


# views.py
class GetAllMessages(ListAPIView):
    queryset = Request.objects.all().order_by('-created_at')
    serializer_class = RequestSerializer
    pagination_class = None


class TodayNewViewListAPIView(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = None

    def get_queryset(self):
        today = timezone.now().date()
        return Request.objects.filter(created_at__date=today)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({"count": count})


class UnreadNewCountListView(ListAPIView):
    queryset = Request.objects.all().count()
    serializer_class = RequestSerializer
    pagination_class = None

    def get_queryset(self):
        return Request.objects.filter(is_read=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({"count": count})
