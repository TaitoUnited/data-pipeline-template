import os
from django.http import JsonResponse
from django.db import connection
from project.config import Config
from common.etl import storage


def get_config(request):
    client_config = {
        "APP_VERSION": Config.APP_VERSION,
    }
    return JsonResponse({"data": client_config})


def get_uptimez(request):
    # Check database
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

    # Check storage bucket
    bucket = storage.create_storage_bucket_client(os.environ["STORAGE_BUCKET"])
    bucket.health()

    # OK
    return JsonResponse({"status": "OK"})


def get_healthz(request):
    return JsonResponse({"status": "OK"})
