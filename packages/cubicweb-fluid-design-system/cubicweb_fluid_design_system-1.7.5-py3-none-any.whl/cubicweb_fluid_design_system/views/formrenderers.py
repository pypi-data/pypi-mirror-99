# copyright 2013-2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.
"""fluid_design_system implementation of formrenderers"""

__docformat__ = "restructuredtext en"

from warnings import warn

from logilab.common.decorators import monkeypatch

from cubicweb import tags
from cubicweb.utils import support_args
from cubicweb.web.views import formrenderers


@monkeypatch(formrenderers.EntityCompositeFormRenderer)
def render_fields(self, w, form, values):
    if form.parent_form is None:
        # We should probably take those CSS classes to uiprops.py
        w(u'<table class="table table-striped table-bordered table-condensed">')
        # get fields from the first subform with something to display (we
        # may have subforms with nothing editable that will simply be
        # skipped later)
        for subform in form.forms:
            subfields = [field for field in subform.fields
                         if field.is_visible()]
            if subfields:
                break
        if subfields:
            # main form, display table headers HTML5
            w(u'<thead>')
            w(u'<tr>')
            w(u'<th>%s</th>' %
              tags.input(type='checkbox',
                         title=self._cw._('toggle check boxes'),
                         onclick="setCheckboxesState('eid', null, this.checked)"))
            for field in subfields:
                w(u'<th>%s</th>' % formrenderers.field_label(form, field))
            w(u'</tr>')
            w(u'</thead>')
    super(formrenderers.EntityCompositeFormRenderer, self).render_fields(w, form, values)
    if form.parent_form is None:
        w(u'</table>')
        if self._main_display_fields:
            super(formrenderers.EntityCompositeFormRenderer, self)._render_fields(
                self._main_display_fields, w, form)


formrenderers.FormRenderer.button_bar_class = u'form-group'


class ModalFormRenderer(formrenderers.FormRenderer):
    __regid__ = 'modal-form-renderer'
    button_bar_class = 'modal-footer'

    def open_form(self, form, values, **attrs):
        showmessage = values.get('showmessage')
        showonload = values.get('showonload', False)
        if showonload:
            # show the `modal` dialog : initialized in
            # basecomponents.CookieLoginComponent by showonload=True
            self._cw.add_onload("$('#%s').modal('show')" % values['modal_id'])
            data_backdrop, data_keyboard = u'static', u'false'
        else:
            data_backdrop, data_keyboard = u'true', u'true'

        html = [u'<div class="%(class)s" id="%(id)s" tabindex="-1" role="dialog" '
                u'data-backdrop="%(backdrop)s" data-keyboard="%(keyboard)s">\n'
                u'<div class="modal-dialog">'
                u'<div class="modal-content">' % {
                    'id': values['modal_id'],
                    'class': u'modal fade in' if showmessage else u'modal',
                    'backdrop': data_backdrop, 'keyboard': data_keyboard}]
        html.append(super(ModalFormRenderer, self).open_form(form, values, **attrs))
        html.append(u'<div class="modal-header">')
        if not showonload:
            # add cancel button when modal triggered by CookieLoginComponent
            html.append(u'<button type="button" class="close" data-dismiss="modal" '
                        'aria-hidden="true">&#215;</button>')
        html.append(
            u'<div class="modal-title">%s</div>\n</div>\n' % values.get('title', u''))
        return u'\n'.join(html)

    def render_content(self, w, form, values):
        self._cw.add_onload("$('.close').click(function () {$(this).parent().removeClass('in');});")
        w(u'<div class="modal-body">')
        if values.get('showmessage'):
            message = self._cw.message
            if message:
                w(u'<div class="alert alert-danger in">%s'
                  u'<button class="close" data-dismiss="alert">x</button></div>' % message)
        if self.display_progress_div:
            w(u'<div id="progress">%s</div>' % self._cw._('validating...'))
        w(u'\n<fieldset>\n')
        self.render_fields(w, form, values)
        w(u'\n</fieldset>\n')
        w(u'</div>')
        self.render_buttons(w, form)

    def close_form(self, form, values):
        html = [super(ModalFormRenderer, self).close_form(form, values)]
        html.append('</div></div></div>')  # close modal-content, modal-dialog, ...
        return u'\n'.join(html)


@monkeypatch(formrenderers.FormRenderer)
def render_help(self, form, field):
    """display help in the form
    """
    help = []
    descr = field.help
    if callable(descr):
        if support_args(descr, 'form', 'field'):
            descr = descr(form, field)
        else:
            warn("[3.10] field's help callback must now take form "
                 "and field as argument (%s)" % field, DeprecationWarning)
            descr = descr(form)
    if descr:
        help.append('<p class="help-block">%s</p>' % self._cw._(descr))
    example = field.example_format(self._cw)
    if example:
        help.append('<p class="form-control-static">(%s: %s)</p>'
                    % (self._cw._('sample format'), example))
    return u'&#160;'.join(help)


@monkeypatch(formrenderers.FormRenderer)
def error_message(self, form):
    """return formatted error message

    This method should be called once inlined field errors has been consumed
    """
    req = self._cw
    errex = form.form_valerror
    # get extra errors
    if errex is not None:
        errormsg = req._('please correct the following errors:')
        errors = form.remaining_errors()
        if errors:
            if len(errors) > 1:
                templstr = u'<li>%s</li>'
            else:
                templstr = u'&#160;%s'
            for field, err in errors:
                if field is None:
                    errormsg += templstr % err
                else:
                    errormsg += templstr % '%s: %s' % (req._(field), err)
            if len(errors) > 1:
                errormsg = '<ul>%s</ul>' % errormsg
        return u'<div class="alert alert-danger">%s</div>' % errormsg
    return u''


@monkeypatch(formrenderers.FormRenderer)
def _render_fields(self, fields, w, form):
    """render form fields
    """
    byfieldset = {}
    for field in fields:
        byfieldset.setdefault(field.fieldset, []).append(field)
    if form.fieldsets_in_order:
        fieldsets = form.fieldsets_in_order
    else:
        fieldsets = byfieldset
    for fieldset in list(fieldsets):
        try:
            fields = byfieldset.pop(fieldset)
        except KeyError:
            self.warning('no such fieldset: %s (%s)', fieldset, form)
            continue
        w(u'<fieldset>\n')
        if fieldset:
            w(u'<legend>%s</legend>' % self._cw.__(fieldset))
        for field in fields:
            error = form.field_error(field)
            control = not hasattr(field, 'control_field') or field.control_field
            w(u'<div id="%s-%s_row" class="form-group %s">' % (
                field.name, field.role, 'error' if error else ''))
            if self.display_label and field.label is not None:
                w(u'%s' % self.render_label(form, field))
            # Use full width for inlined forms, 9/12 for normal fields
            base_css = 'col-md-12' if hasattr(field, 'view') else 'col-md-9'
            if not control:
                # katia : 'control' class no longer exists in fluid_design_system 3.0.0
                # but is used here because of
                # 'form-horizontal' fluid_design_system 2.0.4 css
                # backport
                base_css += ' nomargin'
            w(u'<div class="%s">' % base_css)
            w(field.render(form, self))
            if error:
                self.render_error(w, error)
            if self.display_help:
                w(self.render_help(form, field))
            w(u'</div>')
            w(u'</div>')
        w(u'</fieldset>')
    if byfieldset:
        self.warning('unused fieldsets: %s', ', '.join(byfieldset))


@monkeypatch(formrenderers.FormRenderer)
def render_label(self, form, field):
    if field.label is None:
        return u''
    label = formrenderers.field_label(form, field)
    attrs = {'for': field.dom_id(form)}
    attrs['class'] = 'col-md-3 control-label'
    if field.required:
        attrs['class'] += ' required'
    return tags.label(label, **attrs)


@monkeypatch(formrenderers.FormRenderer)
def render_buttons(self, w, form):
    """render form's buttons
    """
    if not form.form_buttons:
        return
    w(u'<div class="%s">' % self.button_bar_class)
    for button in form.form_buttons:
        w(button.render(form))
    w(u'</div>')


@monkeypatch(formrenderers.EntityFormRenderer)
def open_form(self, form, values):
    attrs_fs_label = u''
    if self.main_form_title:
        attrs_fs_label = u'<h3>%s</h3>' % self._cw._(self.main_form_title)
    open_form = attrs_fs_label + super(formrenderers.EntityFormRenderer,
                                       self).open_form(form, values)
    return open_form


@monkeypatch(formrenderers.EntityFormRenderer)
def close_form(self, form, values):
    # needed to remove the '</div>' from the original method
    return super(formrenderers.EntityFormRenderer, self).close_form(form, values)


@monkeypatch(formrenderers.EntityFormRenderer)  # noqa: F811
def render_buttons(self, w, form):
    # needed to use our own monkeypatched FormRenderer.render_buttons() which
    # doesn't need to add a special case when there are 3 buttons to render
    super(formrenderers.EntityFormRenderer, self).render_buttons(w, form)


@monkeypatch(formrenderers.EntityInlinedFormRenderer)  # noqa: F811
def open_form(self, w, form, values):
    try:
        w(u'<div id="div-%(divid)s" onclick="%(divonclick)s">' % values)
    except KeyError:
        w(u'<div id="div-%(divid)s">' % values)
    else:
        w(u'<div id="notice-%s" class="notice text-info">'
          u'<span class="glyphicon glyphicon-info-sign"></span> %s</div>' % (
              values['divid'], self._cw._('click on the box to cancel the deletion')))
    w(u'<div class="iformBody">')


@monkeypatch(formrenderers.EntityInlinedFormRenderer)  # noqa: F811
def close_form(self, w, form, values):
    w(u'</div></div>')


@monkeypatch(formrenderers.EntityInlinedFormRenderer)  # noqa: F811
def render_fields(self, w, form, values):
    w(u'<fieldset id="fs-%(divid)s">' % values)
    fields = self._render_hidden_fields(w, form)
    w(u'</fieldset>')
    if fields:
        self._render_fields(fields, w, form)
    self.render_child_forms(w, form, values)
