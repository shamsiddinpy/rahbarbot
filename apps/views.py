from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
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
    permission_classes = [AllowAny, ]
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Request"])
@api_view(['GET'])
def get_message_count(request):
    count = Request.objects.count()
    return Response({"count": count})


# views.py

@api_view(['GET'])
def get_all_messages(request):
    all_requests = Request.objects.all().order_by('-created_at')
    data = []
    for req in all_requests:
        attachment_url = None
        if req.attachment:
            attachment_url = request.build_absolute_uri(req.attachment.url)
        data.append({
            "id": req.id,
            "user_id": req.user.id if req.user else None,
            "username": req.user.username if req.user else "Unknown User",
            "reason": req.reason,
            "attachment_url": attachment_url,
            "user_info": req.full_name,
            "phone_number": req.phone_number,
            "created_at": req.created_at.isoformat() if req.created_at else None
        })

    return JsonResponse({"messages": data})


# @api_view(['GET'])
# def list_anonymous_requests(request):
#     anonymous_qs = Request.objects.filter(is_anonymous=True).order_by('-created_at')
#
#     data = []
#     for req in anonymous_qs:
#         attachment_url = None
#         if req.attachment:
#             attachment_url = request.build_absolute_uri(req.attachment.url)
#
#         data.append({
#             "id": req.id,
#             "reason": req.reason,
#             "attachment": attachment_url,
#             "created_at": req.created_at.isoformat() if req.created_at else None,
#         })
#
#     return JsonResponse({"anonymous_requests": data})


@api_view(['GET'])
def today_new(request):
    today = timezone.now().date()
    count_today = Request.objects.filter(created_at__date=today).count()
    return JsonResponse({"today": count_today})


@api_view(['GET'])
def unread_new_count(request):
    count_unread = Request.objects.filter(is_read=False).count()
    return JsonResponse({"unread": count_unread})
