class CSPAwareWidget:
    """ A widget wrapper class that injects a CSP nonce into the template context """
    def __init__(self, widget, csp_nonce):
        self.widget = widget
        self.csp_nonce = csp_nonce

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['csp_nonce'] = self.csp_nonce
        return self._render(self.template_name, context, renderer)

    def __getattr__(self, attr):
        return getattr(self.widget, attr)


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
            if hasattr(self, 'csp_nonce'):
                for k, v in self.fields.items():
                    self.fields[k].widget = CSPAwareWidget(self.fields[k].widget, self.csp_nonce)

        else:
            super().__init__(*args, **kwargs)
