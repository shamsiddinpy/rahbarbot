import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook(request):
    try:
        if request.method == "POST":
            payload = json.loads(request.body)
            return JsonResponse({"status": "success"}, status=200)
        return JsonResponse({"error": "Method not allowed"}, status=405)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received.")
        return JsonResponse({"error": "Invalid JSON"}, status=400)
