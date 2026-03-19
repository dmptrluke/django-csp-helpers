def get_nonce(request):
    """Return the CSP nonce from the request, supporting both django-csp and Django 6+ native CSP."""
    # django-csp middleware sets request.csp_nonce
    nonce = getattr(request, 'csp_nonce', None)
    if nonce is not None:
        return nonce

    # Django 6+ native CSP middleware sets request._csp_nonce
    try:
        from django.middleware.csp import get_nonce as _get_nonce

        return _get_nonce(request)
    except ImportError:
        return None


def get_nonce_from_context(context):
    """Return the CSP nonce from a template context, supporting both django-csp and Django 6+ native CSP."""
    # Django 6+ context processor sets csp_nonce directly in context
    nonce = context.get('csp_nonce')
    if nonce is not None:
        return nonce

    # Fall back to reading from the request object
    request = context.get('request')
    if request is not None:
        return get_nonce(request)

    return None
