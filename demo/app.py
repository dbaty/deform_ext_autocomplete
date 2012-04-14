"""A Pyramid application that demonstrates the widget.

Instructions:

1. Install Pyramid.
2. Install deform_ext_autocomplete.
3. Run "python app.py".

An HTTP server will listen on port 61523: http://0.0.0.0:61523
"""

import os

from colander import Schema
from colander import SchemaNode
from colander import SequenceSchema
from colander import String

from deform import Form
from deform import ValidationFailure
from deform.widget import SequenceWidget

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPSeeOther

from deform_ext_autocomplete import ExtendedAutocompleteInputWidget
from deform_ext_autocomplete import includeme


PERSONS = {'jhendrix': 'Jimi Hendrix',
           'jpage': 'Jimmy Page',
           'jbonham': 'John Bonham',
           'bcobham': 'Billy Cobham'}


class Person(SequenceSchema):
    person = SchemaNode(
        String(),
        widget=ExtendedAutocompleteInputWidget(
            display_value=lambda field, person_id: PERSONS.get(person_id, ''),
            values='/ajax_search'))


class DemoSchema(Schema):
    persons = Person(widget=SequenceWidget(min_len=1))


def make_form(request, action):
    schema = DemoSchema().bind(request=request)
    return Form(schema, action=action, buttons=('Save changes', ))


def add_form(request, form=None):
    if form is None:
        form = make_form(request, request.route_url('add'))
    return {'request': request,
            'persons': sorted(PERSONS.values()),
            'rendered_form': form.render()}


def _validate_and_redirect(request, view, route):
    """Validate form and redirect to the add/edit form or the success
    page.
    """
    form = make_form(request, request.route_url(route))
    try:
        data = form.validate(request.POST.items())
    except ValidationFailure, e:
        return view(request, e)
    url = request.route_url('saved', _query={'saved': unicode(data)})
    return HTTPSeeOther(url)


def save(request):
    return _validate_and_redirect(request, add_form, 'add')


def saved(request):
    return {'request': request,
            'saved': request.GET['saved']}


def edit_form(request, form=None):
    if form is None:
        form = make_form(request , request.route_url('edit'))
        form_data = {'persons': ('jpage', 'jbonham')}
        form = form.render(form_data)
    else:
        form = form.render()
    return {'rendered_form': form}


def edit(request):
    return _validate_and_redirect(request, edit_form, 'edit')


def readonly(request):
    form = make_form(request , 'there-is-no-action')
    form_data = {'persons': ('jpage', 'jbonham')}
    form = form.render(form_data, readonly=True)
    return {'rendered_form': form}


def highlight_term(term, s, pattern='<strong>%s</strong>'):
    """Highlight ``term`` in ``s`` by replacing it using the given
    ``pattern``.
    """
    term = term.lower()
    term_len = len(term)
    i = 0
    highlighted = ''
    while i < len(s):
        window = s[i:i + term_len]
        if window.lower() == term:
            highlighted += pattern % window
            i += term_len
        else:
            highlighted += s[i]
            i += 1
    return highlighted


def ajax_search(request):
    term = request.GET['term'].lower()
    res = []
    for person_id, name in PERSONS.items():
        if term not in name.lower():
            continue
        dropdown = highlight_term(term, name)
        res.append({'dropdown': dropdown,
                    'displayed': name,
                    'stored': person_id})
    return res


def get_template_path(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return os.path.abspath(path)


def make_app(global_config, **settings):
    add_pt = get_template_path('add.pt')
    edit_pt = get_template_path('edit.pt')
    saved_pt = get_template_path('saved.pt')
    readonly_pt = get_template_path('readonly.pt')
    config = Configurator(settings=settings)
    config.add_route('add', '/')
    config.add_view(add_form, route_name='add',
                    request_method='GET',
                    renderer=add_pt)
    config.add_view(save, route_name='add',
                    request_method='POST',
                    renderer=add_pt)
    config.add_route('saved', '/saved')
    config.add_view(saved, route_name='saved',
                    renderer=saved_pt)
    config.add_route('edit', '/edit')
    config.add_view(edit_form, route_name='edit', request_method='GET',
                    renderer=edit_pt)
    config.add_view(edit, route_name='edit', request_method='POST',
                    renderer=edit_pt)
    config.add_route('readonly', '/readonly')
    config.add_view(readonly, route_name='readonly', renderer=readonly_pt)
    config.add_route('ajax_search', '/ajax_search')
    config.add_view(ajax_search, route_name='ajax_search',
                    xhr=True, renderer='json')
    config.add_static_view('static', 'deform:static')
    includeme(config)
    return config.make_wsgi_app()


if __name__ == '__main__':
    from waitress import serve
    serve(make_app({}), port=61523, expose_tracebacks=True)
