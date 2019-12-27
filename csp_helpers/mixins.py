from csp_helpers.classes import CSPAwareMedia, CSPAwareWidget


class CSPViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request, 'csp_nonce'):
            kwargs.update({'csp_nonce': self.request.csp_nonce})
        return kwargs


class CSPFormMixin:
    def __init__(self, *args, **kwargs):
        if 'csp_nonce' in kwargs:
            self.csp_nonce = kwargs.pop('csp_nonce')
            super().__init__(*args, **kwargs)

            for k, v in self.fields.items():
                self.fields[k].widget = CSPAwareWidget(self.fields[k].widget, self.csp_nonce)

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
