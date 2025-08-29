from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Let DRF handle the exception first
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error response
        return Response({
            "success": False,
            "message": "Validation failed" if response.status_code == 400 else "Error occurred",
            "errors": response.data
        }, status=response.status_code)

    # If it's not handled by DRF (e.g. server error), fallback
    return Response({
        "success": False,
        "message": "Something went wrong on the server",
        "errors": {}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
