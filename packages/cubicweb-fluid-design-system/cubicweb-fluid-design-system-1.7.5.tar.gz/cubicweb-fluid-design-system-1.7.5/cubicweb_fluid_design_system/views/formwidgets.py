"""fluid_design_system implementation of formwidgets

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.common.decorators import monkeypatch
from logilab.mtconverter import xml_escape

from cubicweb import tags, __version__ as cwver
from cubicweb.web import formwidgets

from cubicweb_fluid_design_system import CW_325


# Buttons
@monkeypatch(formwidgets.Button)
def render(self, form, field=None, renderer=None):
    label = form._cw._(self.label)
    attrs = self.attrs.copy()
    if not cwver.startswith('3.20'):
        # 3.21 commit b0417cacecd9
        attrs.setdefault('class', self.css_class)
    if self.cwaction:
        assert self.onclick is None
        attrs['onclick'] = "postForm('__action_%s', \'%s\', \'%s\')" % (
            self.cwaction, self.label, form.domid)
    elif self.onclick:
        attrs['onclick'] = self.onclick
    if self.name:
        attrs['name'] = self.name
        if self.setdomid:
            attrs['id'] = self.name
    if not CW_325:
        if self.settabindex and 'tabindex' not in attrs:
            attrs['tabindex'] = form._cw.next_tabindex()
    if self.icon:
        img = u'<i class="%s"> </i>' % self.icon
    else:
        img = u''
    return tags.button(img + xml_escape(label), escapecontent=False,
                       value=label, type=self.type, **attrs)
