from itertools import chain

from django.forms import Media
from django.utils.html import format_html


class CSPAwareMedia(Media):
    def __init__(self, *args, **kwargs):
        if 'csp_nonce' in kwargs:
            self.csp_nonce = kwargs.pop('csp_nonce')

        super().__init__(*args, **kwargs)
        pass

    def render_js(self):
        if hasattr(self, 'csp_nonce'):
            return [
                format_html(
                    '<script type="text/javascript" src="{}" nonce="{}"></script>',
                    self.absolute_path(path),
                    self.csp_nonce
                ) for path in self._js
            ]
        else:
            return super().render_js()

    def render_css(self):
        if hasattr(self, 'csp_nonce'):
            media = sorted(self._css)
            return chain.from_iterable([
                format_html(
                    '<link href="{}" type="text/css" media="{}" nonce="{}" rel="stylesheet">',
                    self.absolute_path(path), medium, self.csp_nonce
                ) for path in self._css[medium]
            ] for medium in media)
        else:
            return super().render_css()

    def __add__(self, other):
        combined = CSPAwareMedia(csp_nonce=self.csp_nonce)
        combined._css_lists = self._css_lists + other._css_lists
        combined._js_lists = self._js_lists + other._js_lists
        return combined


__all__ = ['CSPAwareMedia']
