import types

from csp_helpers.classes import CSPAwareMedia
from csp_helpers.utils import get_nonce


def patched_render(self, name, value, attrs=None, renderer=None):
    context = self.get_context(name, value, attrs)
    context['csp_nonce'] = self.csp_nonce
    return self._render(self.template_name, context, renderer)


class CSPFormMixin:
    def __init__(self, *args, **kwargs):
        if 'csp_nonce' in kwargs:
            self.csp_nonce = kwargs.pop('csp_nonce')
            super().__init__(*args, **kwargs)

            for _name, field in self.fields.items():
                # monkeypatch the widget!
                field.widget.csp_nonce = self.csp_nonce
                field.widget.render = types.MethodType(patched_render, field.widget)

        else:
            super().__init__(*args, **kwargs)

    @property
    def media(self):
        """Return all media required to render the widgets on this form."""
        if hasattr(self, 'csp_nonce'):
            media = CSPAwareMedia(csp_nonce=self.csp_nonce)
            for field in self.fields.values():
                media = media + field.widget.media
            return media
        return super().media


class CSPViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        nonce = get_nonce(self.request)
        if nonce is not None:
            kwargs['csp_nonce'] = nonce
        return kwargs
