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
