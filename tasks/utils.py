from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Global DRF exception handler.

    Wraps all error responses in a consistent envelope shape:
        {
            "success": false,
            "errors":  { ... field-level or non-field errors ... },
            "status":  <HTTP status code>
        }

    Registered in settings.py under REST_FRAMEWORK['EXCEPTION_HANDLER'].
    Unhandled exceptions (500s) are passed through unchanged so Django's
    default error handling still applies.
    """
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'success': False,
            'errors':  response.data,
            'status':  response.status_code,
        }
    return response