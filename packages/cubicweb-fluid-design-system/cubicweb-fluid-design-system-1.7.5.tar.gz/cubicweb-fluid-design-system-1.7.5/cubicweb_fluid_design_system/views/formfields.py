"""fluid_design_system implementation of formfields

:organization: Logilab
:copyright: 2015 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.common.decorators import monkeypatch

from cubicweb.utils import UStringIO
from cubicweb.web import formfields


@monkeypatch(formfields.FileField)
def render_subfield(self, form, field, renderer):
    data = UStringIO()  # XXX add support for tracewrites
    w = data.write
    w(u'<div class="row">')
    w(renderer.render_label(form, field))
    w(u'<div class="col-md-9">')
    w(field.render(form, renderer))
    w(u'</div>')
    w(u'</div>')
    w(u'<div class="row">')
    w(u'<div class="col-md-offset-3 col-md-9">')
    w(renderer.render_help(form, field))
    w(u'</div>')
    w(u'</div>')
    return data.getvalue()
