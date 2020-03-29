import json
from pkg_resources import resource_filename

from colander import null

import deform
from deform.compat import string_types
from deform.widget import AutocompleteInputWidget


def includeme(config, deform=deform):
    """Call this function to enable the widget (more precisely,
    register the widget templates) or add "deform_ext_autocomplete" in
    the ``pyramid.includes`` directive of your Pyramid configuration
    file.

    The ``deform`` argument should only be used in tests.
    """
    search_path = list(deform.Form.default_renderer.loader.search_path)
    path = resource_filename('deform_ext_autocomplete', 'templates')
    search_path.append(path)
    static_path = resource_filename('deform_ext_autocomplete', 'static')
    config.add_static_view(static_path, 'deform_ext_autocomplete:static')
    deform.Form.default_renderer.loader.search_path = search_path
    config.include('pyramid_chameleon')


class ExtendedAutocompleteInputWidget(AutocompleteInputWidget):
    """Render an ``<input type="text"/>`` widget which provides
    autocompletion via a list of values.

    Contrary to :py:class:`deform.widget.AutocompleteInputWidget`, it
    can store a value that is different from the one it displays. The
    attributes and arguments are the same as those of
    :py:class:`deform.widget.AutocompleteInputWidget` except the
    following ones which replace or add to the former:

    **Attributes/Arguments**

    template
        The template name used to render the widget.  Default:
        ``autocomplete_input_w_hidden``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/autocomplete_input_w_hidden``.

    values
        Either an iterable that can be converted to a JSON array, or a
        string representing a URL. If the latter, an XMLHTTPRequest
        will be sent to this URL to retrieve a JSON serialization of
        an iterable. In either case, each value of the iterable must
        be an associative array that has at least two keys: ``stored``
        and ``displayed``. Both values must be strings. An optional
        ``dropdown`` key may be provided, in which case it will be
        used in the dropdown that appears when the user starts typing
        characters in the text input widget. Default: ``()`` (the
        empty tuple).

    display_value
        A callable that accepts two arguments: the field and the
        ``cstruct`` (which usually corresponds to the value that is to
        be stored -- see `Colander
        <http://docs.pylonsproject.org/projects/colander/en/latest/index.html>`_
        documentation for further details). This callable should
        return a string or unicode object that will be displayed in
        the visible text input field once the user has selected an
        item. Note that ``cstruct`` may be the empty string when the
        field has not been filled. Default: ``lambda widget, field,
        cstruct: cstruct``

    strip
        If true, during deserialization, strip the value of leading
        and trailing whitespace. Default: ``True``.

    min_length
        ``min_length`` is the number of characters to wait for before
        activating the autocomplete call. Default: ``1``.

    delay
        ``delay`` is the number of milliseconds to wait for before
        activating the autocomplete call. Default: ``400`` (ms) if
        values are fetched via AJAX, ``10`` (ms) otherwise.
    """
    template = 'ext_autocomplete_input'
    readonly_template = 'readonly/ext_autocomplete_input'
    values = ()
    display_value = lambda widget, field, cstruct: cstruct
    strip = True
    min_length = 1
    delay = None  # varying default, see `serialize()`

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        options = {}
        delay = getattr(self, 'delay', None)
        if delay is None:
            if isinstance(self.values, string_types):
                delay = 400
            else:
                delay = 10
        options['delay'] = delay
        options['minLength'] = self.min_length
        options = json.dumps(options)
        values = json.dumps(self.values)
        template = readonly and self.readonly_template or self.template
        visible_cstruct = self.display_value(field, cstruct)
        return field.renderer(template,
                              cstruct=cstruct,  # hidden field
                              visible_cstruct=visible_cstruct,
                              field=field,
                              options=options,
                              values=values)
