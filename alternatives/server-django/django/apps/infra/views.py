from django.http import JsonResponse
from django.db import connection
from project.config import Config


def get_config(request):
    client_config = {
        "APP_VERSION": Config.APP_VERSION,
    }
    return JsonResponse({"data": client_config})


def get_uptimez(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "OK"})


def get_healthz(request):
    return JsonResponse({"status": "OK"})
