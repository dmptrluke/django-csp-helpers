from .wrappers import CSPAwareWidget


class CSPViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'csp_nonce': self.request.csp_nonce})
        return kwargs


class CSPFormMixin:
    def __init__(self, *args, **kwargs):
        self.csp_nonce = kwargs.pop('csp_nonce')
        super().__init__(*args, **kwargs)

        for k, v in self.fields.items():
            self.fields[k].widget = CSPAwareWidget(self.fields[k].widget, self.csp_nonce)
