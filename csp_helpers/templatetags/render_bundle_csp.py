from django import template
from django.utils.safestring import mark_safe

from csp_helpers.utils import get_nonce_from_context

try:
    import webpack_loader
except ImportError:
    webpack_loader = None

register = template.Library()


def render_bundle_csp(context, bundle_name, extension=None, config='DEFAULT', attrs=''):
    nonce = get_nonce_from_context(context)
    if nonce is not None:
        attrs = ' '.join([attrs, f'nonce="{nonce}"'])

    tags = webpack_loader.utils.get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))


if webpack_loader is not None:
    register.simple_tag(render_bundle_csp, takes_context=True)
