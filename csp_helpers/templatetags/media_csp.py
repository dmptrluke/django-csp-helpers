from itertools import chain

from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def media_csp(context, _form):
    """
    A template tag that takes a Form object in a request context,
     and spits out the correct tags with CSP nonces.
    """
    tags = []

    for url in _form.media._js:
        tags.append(
            f'<script type="text/javascript" src="{static(url)}" nonce="{context.request.csp_nonce}"></script>'
        )

    # I didn't write this. This comes from Django.
    tags += chain.from_iterable([
        format_html(
            '<link href="{}" type="text/css" media="{}" rel="stylesheet" nonce="{}">',
            static(path), medium, context.request.csp_nonce
        ) for path in _form.media._css[medium]
    ] for medium in sorted(_form.media._css))

    return mark_safe('\n'.join(tags))
