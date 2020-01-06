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

### How to use
Simply add **CSPViewMixin** to your Views, and **CSPFormMixin** to your Forms or ModelForms.
You will need to use *both* mixins together, they don't work alone.

**CSPFormMixin**
```python
from csp_helpers.mixins import CSPFormMixin

class ArticleForm(CSPFormMixin, ModelForm):
    ...
```

**CSPViewMixin**
```python
from csp_helpers.mixins import CSPViewMixin
from .forms import ArticleForm

class ArticleUpdateView(CSPViewMixin, UpdateView):
    form_class = ArticleForm
    ...
```

#### Using only CSPFormMixin
If you are managing your form manually, or not using class-based views, you will not be able
to use **CSPViewMixin**. In these cases, just call your form with `csp_nonce` as an argument
manually, like below.

```python
form = ArticleForm(csp_nonce=request.csp_nonce)
```


### What it does
The *django-csp-helpers* mixins will modify and extend your views and forms in two ways.

#### Form Widgets
Form widgets will be patched to inject a CSP nonce into the rendering context for template
widgets. You can access this with `{{ csp_nonce }}` in your widget templates.

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