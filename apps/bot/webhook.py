# apps/bot/views.py
import json
import logging

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from apps.bot import handler

logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            update = Update.de_json(data, handler.bot)
            handler.dp.process_update(update)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.exception("Webhookda xatolik: %s", e)
            return HttpResponseBadRequest("Noto'g'ri so'rov")
    else:
        return JsonResponse({"status": "faqat POST so'rovlari qabul qilinadi"}, status=405)
