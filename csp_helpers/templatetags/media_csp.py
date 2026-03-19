from itertools import chain

from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from csp_helpers.utils import get_nonce_from_context

register = template.Library()


@register.simple_tag(takes_context=True)
def media_csp(context, _form):
    """
    A template tag that takes a Form object in a request context,
     and spits out the correct tags with CSP nonces.
    """
    nonce = get_nonce_from_context(context)
    tags = []

    # fmt: off
    for url in _form.media._js:
        tags.append(
            format_html(
                '<script type="text/javascript" src="{}" nonce="{}"></script>',
                static(url), nonce
            )
        )

    tags += chain.from_iterable([
        format_html(
            '<link href="{}" type="text/css" media="{}" rel="stylesheet" nonce="{}">',
            static(path), medium, nonce
        ) for path in _form.media._css[medium]
    ] for medium in sorted(_form.media._css))
    # fmt: on

    return mark_safe('\n'.join(tags))
