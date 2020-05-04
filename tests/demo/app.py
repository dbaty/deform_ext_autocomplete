"""A Pyramid application that demonstrates the widget.

Instructions:

1. Install pyramid_chameleon.
2. Install waitress
3. Install deform_ext_autocomplete.
4. Run "python app.py".

An HTTP server will listen on port 61523: http://0.0.0.0:61523
"""

import itertools
import json
import os

from colander import Schema
from colander import SchemaNode
from colander import SequenceSchema
from colander import String
from deform import Form
from deform import ValidationFailure
from deform.widget import HiddenWidget
from deform.widget import SequenceWidget
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPSeeOther

from deform_ext_autocomplete import ExtendedAutocompleteInputWidget
from deform_ext_autocomplete import includeme


PERSONS = {'jhendrix': 'Jimi Hendrix',
           'jpage': 'Jimmy Page',
           'jbonham': 'John Bonham',
           'bcobham': 'Billy Cobham'}


# We need a unique counter shared by all forms. Otherwise a distinct
# (but identical) counter is used for each form and it generates the
# same field identifiers for each form, which breaks our code. We
# would not need that if we only had a single form on the page.
FORM_ID_COUNTER = itertools.count()


PersonNode = SchemaNode(
    String(),
    widget=ExtendedAutocompleteInputWidget(
        display_value=lambda field, person_id: PERSONS.get(person_id, ''),
        values='/ajax_search')
)


class Person(SequenceSchema):
    person = PersonNode


class DemoSchemaMultiple(Schema):
    persons = Person(widget=SequenceWidget(min_len=1))


class DemoSchemaSingle(Schema):
    person = PersonNode


def make_form(request, form_class, form_name):
    schema = form_class().bind(request=request)
    schema.add(
        SchemaNode(
            String(),
            name='submitted_form',
            default=form_name,
            widget=HiddenWidget(),
        )
    )
    action = request.route_url('index')
    return Form(
        schema,
        formid=form_name,
        counter=FORM_ID_COUNTER,
        action=action,
        buttons=['Save'],
    )


def index(request):
    # Initialize all forms.
    add_form_single = make_form(request, DemoSchemaSingle, 'add_single')
    add_form_multiple = make_form(request, DemoSchemaMultiple, 'add_multiple')
    edit_form_multiple = make_form(request, DemoSchemaMultiple, 'edit_multiple')
    read_only_form = make_form(request, DemoSchemaMultiple, 'read_only')

    # Process submitted form (if any).
    submitted_form = None
    if request.method == 'POST':
        submitted_form_name = request.POST['submitted_form']
        submitted_form = {
            'add_single': add_form_single,
            'add_multiple': add_form_multiple,
            'edit_multiple': edit_form_multiple,
        }.get(submitted_form_name)
        if submitted_form is None:
            raise ValueError("Unexpected submitted form: '%s'" % submitted_form)

        try:
            data = submitted_form.validate(request.POST.items())
        except ValidationFailure:
            pass
        else:
            data.pop('submitted_form')
            url = request.route_url('saved', _query='saved=%s' % json.dumps(data))
            return HTTPSeeOther(url)

    # Get requirements before rendering the forms. All forms have the
    # same requirements.
    requirements = add_form_multiple.get_widget_resources()

    # Pre-fill read-only and edit forms (the latter only if it has not
    # been submitted). Render all forms for the template.
    form_data = {'persons': ('jpage', 'jbonham')}
    read_only_form = read_only_form.render(form_data, readonly=True)
    if submitted_form != edit_form_multiple:
        edit_form_multiple = edit_form_multiple.render(form_data)
    else:
        edit_form_multiple = edit_form_multiple.render()
    add_form_single = add_form_single.render()
    add_form_multiple = add_form_multiple.render()

    return {
        'request': request,
        'requirements': requirements,
        'persons': sorted(PERSONS.values()),
        'forms': {
            'add_single': add_form_single,
            'add_multiple': add_form_multiple,
            'edit_multiple': edit_form_multiple,
            'read_only': read_only_form,  # already rendered
        },
    }


def saved(request):
    saved_data = json.loads(request.GET['saved'])
    return {'saved': saved_data}


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

    saved_pt = get_template_path('saved.pt')

    config = Configurator(settings=settings)

    config.add_route('index', '/')
    config.add_view(
        index,
        route_name='index',
        request_method=('GET', 'POST'),
        renderer=get_template_path('index.pt'),
    )

    config.add_route('saved', '/saved')
    config.add_view(saved, route_name='saved',
                    renderer=saved_pt)

    config.add_route('ajax_search', '/ajax_search')
    config.add_view(ajax_search, route_name='ajax_search',
                    xhr=True, renderer='json')

    config.add_static_view('static', 'deform:static')
    includeme(config)
    return config.make_wsgi_app()


if __name__ == '__main__':
    from waitress import serve
    serve(make_app({}), port=61523, expose_tracebacks=True)
