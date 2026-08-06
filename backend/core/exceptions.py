import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


logger = logging.getLogger(__name__)

ERRORS = {
    status.HTTP_400_BAD_REQUEST: ("validation_error", "Les données envoyées sont invalides."),
    status.HTTP_401_UNAUTHORIZED: ("authentication_required", "Authentification requise."),
    status.HTTP_403_FORBIDDEN: ("permission_denied", "Vous n'avez pas la permission d'effectuer cette action."),
    status.HTTP_404_NOT_FOUND: ("not_found", "La ressource demandée est introuvable."),
    status.HTTP_405_METHOD_NOT_ALLOWED: ("method_not_allowed", "Cette méthode HTTP n'est pas autorisée."),
    status.HTTP_409_CONFLICT: ("conflict", "Cette opération entre en conflit avec des données existantes."),
    status.HTTP_429_TOO_MANY_REQUESTS: ("too_many_requests", "Trop de requêtes ont été envoyées."),
}


def api_exception_handler(exc, context):
    """Transforme toutes les erreurs DRF en une structure JSON cohérente."""

    response = exception_handler(exc, context)

    if response is None and isinstance(exc, IntegrityError):
        response = Response(status=status.HTTP_409_CONFLICT)

    if response is None:
        logger.error(
            "Erreur API inattendue dans %s",
            context.get("view"),
            exc_info=(type(exc), exc, exc.__traceback__),
        )
        return Response(
            {
                "error": {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "code": "server_error",
                    "message": "Une erreur interne est survenue.",
                    "details": None,
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    details = response.data
    code, message = ERRORS.get(
        response.status_code,
        ("api_error", "La requête n'a pas pu être traitée."),
    )
    response.data = {
        "error": {
            "status": response.status_code,
            "code": code,
            "message": message,
            "details": details,
        }
    }
    return response
