"""Verificação de saúde usada pelo provedor de homologação e pelo job de deploy (FT-110)."""
from django.conf import settings
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([])
def health(request):
    """Retorna o estado da aplicação e do banco, sem dados de usuários nem segredos."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        database = "ok"
    except Exception:  # noqa: BLE001 - a falha é o próprio resultado da verificação
        database = "indisponivel"
    healthy = database == "ok"
    return Response(
        {"status": "ok" if healthy else "erro", "database": database, "commit": settings.APP_COMMIT},
        status=200 if healthy else 503,
    )
