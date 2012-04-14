.. _advanced:

Advanced examples
=================

Showing yet another value in the dropdown
-----------------------------------------

An optional third key can be added to the associative array in the
``values`` argument/attribute of the widget: ``dropdown``. This value
is displayed in the dropdown menu that may appear when the user starts
typing letters in the autocomplete text input field.

In the example shown in the :ref:`basic` chapter, we show the persons'
name in the dropdown that appears when the user starts typing letters.
We could highlight typed letters in the names. To do so, we provide an
additional ``dropdown`` key in each item of ``values``. The
``ajax_search`` view would then look like this:

.. code-block:: python

   def highlight_term(term, name):
       """Return an HTML representation of ``name`` where ``term`` is
       displayed in bold characters.
       """
       # This is a very naive implementation.
       return name.replace(term, '<strong>%s</strong>' % term)

   def ajax_search(request):
       term = request.GET['term'].lower()
       res = []
       for person_id, name in PERSONS.items():
           if term not in name.lower():
               continue
           dropdown = highlight_term(term, name)
           res.append({'displayed': name,
                       'dropdown': dropdown,
                       'stored': person_id})
       return res

You may note that the ``displayed`` key is left untouched. It should
not be the same as the ``dropdown`` key, as the latter contains HTML
tags, which should not be used for the ``displayed`` key.


An advanced ``display_value`` callable
--------------------------------------

As with any widget in Deform, it is possible to bind the field it is
attached to, so that the field and/or the widget have access to
additional bindings, such as the request.

Here, we will suppose that the persons are stored in a database and
that we can query it through the ``db`` attribute of the request. The
problem is then to access the request from the ``display_value``
callable. To do that, we will define a deferred function:

.. code-block:: python

   import colander

   @colander.deferred
   def deferred_autocomplete_widget(node, kw):
       """Return an instance of ``ExtendedAutocompleteInputWidget``
       where the ``display_value`` callable has access to the database
       connection through the request.
       """
       request = kw['request']
       def display_value(field, cstruct):
           return request.db.find(person_id=cstruct)
       return ExtendedAutocompleteInputWidget(values='/ajax_search',
                                              display_value=display_value)

    class AdvancedSchema(Schema):
        person = SchemaNode(String(),
                            widget=deferred_autocomplete_widget)

    def make_form(request):
        schema = AdvancedSchema().bind(request=request)
        return Form(schema)

Again, this is not related at all to the Extended Autocomplete
widget. This is a pure Colander feature. For further details, see the
`Colander documentation
<http://docs.pylonsproject.org/projects/colander/en/latest/binding.html>`_.