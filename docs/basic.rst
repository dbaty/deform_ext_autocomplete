.. _basic:

Basic example
=============

We'll suppose that you use Pyramid. If not, you may have to adapt some
of the instructions below.

First of all, you need to enable the widget by imperatively calling
the :py:class:`deform_ext_autocomplete.includeme` function, or by
including the ``deform_ext_autocomplete`` string in the
``pyramid.includes`` directive of your Pyramid configuration file.

Extended Autocomplete uses the same arguments/attributes as Deform
defaut :py:class:`deform.widget.AutocompleteInputWidget` and an
additional ``display_value`` argument/attribute which must be a
callable. It must accept two arguments: the field and the `cstruct
<http://docs.pylonsproject.org/projects/colander/en/latest/glossary.html?highlight=cstruct#term-cstruct>`_
(which usually corresponds to the value that is to be stored -- see
`Colander
<http://docs.pylonsproject.org/projects/colander/en/latest/index.html>`_
documentation for further details). This callable should return a
string that will be displayed to the user in the text input field.
This callable is only used when the form has been filled, for
example when redisplaying an add form that has an error, or when
displaying an edit form.

There is a :doc:`demo application <demoapp>` if you want to see it in
action, but here is a basic example of a schema that uses the widget:

.. code-block:: python

   from colander import Schema
   from colander import SchemaNode
   from colander import String

   from deform_ext_autocomplete import ExtendedAutocompleteInputWidget

   PERSONS = {
       'jhendrix': 'Jimi Hendrix',
       'jpage': 'Jimmy Page',
       'jbonham': 'John Bonham',
       'bcobham': 'Billy Cobham',
   }

   def display_value(field, person_id):
       return PERSONS.get(person_id, '')

   class BasicSchema(Schema):
       person = SchemaNode(
           String(),
           widget=ExtendedAutocompleteInputWidget(
               display_value=display_value,
               values='/ajax_search',
           )
       )

The ``values`` argument/attribute must be either an iterable that can
be converted to a JSON array, or a string representing a URL. If the
latter, an XMLHTTPRequest will be sent to this URL to retrieve a JSON
serialization of an iterable. In either case, each value of the
iterable must be an associative array that has at least two keys:
``stored`` and ``displayed``. Both values must be strings.

In Pyramid, here is an example of a view that would return the
required iterable (supposing that the view is configured to return
JSON data):

.. code-block:: python

   def ajax_search(request):
       term = request.GET['term'].lower()
       res = []
       for person_id, name in PERSONS.items():
           if term not in name.lower():
               continue
           res.append({'displayed': name,
                       'stored': person_id})
       return res

The widget provides additional features that are documented in the
:ref:`advanced` chapter.

