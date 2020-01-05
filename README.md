# django-csp-helpers  [![PyPI](https://img.shields.io/pypi/v/django-csp-helpers)](https://pypi.org/project/django-csp-helpers/)
A set of template tags (and mixins!) to assist in building CSP-enabled websites using 
[django-csp](https://github.com/mozilla/django-csp).

## Install

1.  Add "csp_helpers" to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'csp_helpers',
]
```

## Mixins
*django-csp-helpers* includes a pair of mixins that can be applied to views and forms to
allow for the use of CSP nonces in widgets and form media.

Our example scenario is below:

    There is a contact form feature on our website that uses a FormView and
    a Form. We want to add a recaptcha widget to this form, but the widget 
    needs to use Javascript, which means we need a nonce available in the
    widget context. We also need to include external JS files, which means
    the form media needs to be CSP-aware too.

### How to use
Simply add **CSPViewMixin** to your FormViews, and **CSPFormMixin** to your Forms or ModelForms.

```python
from csp_helpers.mixins import CSPFormMixin

class ContactForm(CSPFormMixin, Form):
    ...
```

### What it does
The *django-csp-helpers* mixins will modify and extend your views and forms in two ways.

#### Form Widgets
Form widgets will be wrapped in a **CSPAwareWidget**, which will inject a CSP nonce into
the rendering context for template widgets. You can access this with `{{ csp_nonce }}` in 
your widget templates.

#### Form Media
Form media (CSS and JS) will be included with CSP nonces.

## Template Tags
*django-csp-helpers* also includes a pair of template tags



### render_bundle_csp
An exact replacement for the [django-webpack-loader](https://github.com/owais/django-webpack-loader) 
`render_bundle` tag that includes bundles with CSP nonces.

```djangotemplate
{% load render_bundle_csp %}

{% render_bundle_csp 'main' 'css' %}
{% render_bundle_csp 'main' 'js %}
```

### media_csp
A less advanced version of the form media functionality provided by the mixins above. Simply load this tag
and pass it a form, and it will include the form media with CSP nonces.

```djangotemplate
{% load media_csp %}

{# include form media #}
{% media_csp myform %}

```

## License

This software is released under the MIT license.
```
Copyright (c) 2019-2020 Luke Rogers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```