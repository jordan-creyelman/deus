from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.http import JsonResponse


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        database_status = "available"
        status_code = 200

    except Exception:
        database_status = "unavailable"
        status_code = 503

    return JsonResponse(
        {
            "status": "ok" if status_code == 200 else "error",
            "service": "deus-backend",
            "database": database_status,
        },
        status=status_code,
    )