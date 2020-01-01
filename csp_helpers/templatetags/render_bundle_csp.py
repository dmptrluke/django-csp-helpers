from django import template
from django.utils.safestring import mark_safe

try:
    import webpack_loader
except ImportError:
    webpack_loader = None

register = template.Library()


def render_bundle_csp(context, bundle_name, extension=None, config='DEFAULT', attrs=''):
    try:
        attrs = ' '.join([attrs, f'nonce="{ context.request.csp_nonce }"'])
    except AttributeError:
        # ¯\_(ツ)_/¯
        pass

    tags = webpack_loader.utils.get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))


if webpack_loader is not None:
    register.simple_tag(render_bundle_csp, takes_context=True)
