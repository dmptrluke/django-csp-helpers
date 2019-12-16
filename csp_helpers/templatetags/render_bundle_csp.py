from django import template
from django.utils.safestring import mark_safe

from webpack_loader import utils

register = template.Library()


@register.simple_tag(takes_context=True)
def render_bundle_csp(context, bundle_name, extension=None, config='DEFAULT', attrs=''):
    try:
        attrs += f'nonce="{ context.request.csp_nonce }"'
    except AttributeError:
        # ¯\_(ツ)_/¯
        pass

    tags = utils.get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))
