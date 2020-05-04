from unittest import TestCase


class TestWidget(TestCase):

    def _makeOne(self, **kwargs):
        from deform_ext_autocomplete import ExtendedAutocompleteInputWidget
        return ExtendedAutocompleteInputWidget(**kwargs)

    def test_deserialize_null(self):
        import colander
        schema = DummySchema()
        field = DummyField(schema)
        widget = self._makeOne()
        pstruct = colander.null
        self.assertEqual(widget.deserialize(field, pstruct), colander.null)

    def test_deserialize_empty(self):
        import colander
        schema = DummySchema()
        field = DummyField(schema, name='person')
        widget = self._makeOne()
        pstruct = ''
        self.assertEqual(widget.deserialize(field, pstruct), colander.null)

    def test_deserialize_filled(self):
        schema = DummySchema()
        field = DummyField(schema, name='person')
        widget = self._makeOne()
        pstruct = 'jsmith'
        self.assertEqual(widget.deserialize(field, pstruct), 'jsmith')

    # The tests below have all been copied from
    # 'deform.tests.test_widget.TestAutocompleteInputWidget'
    def test_serialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        field = DummyField(None, renderer=renderer)
        widget.serialize(field, null)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_None(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        field = DummyField(None, renderer=renderer)
        widget.serialize(field, None)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_url(self):
        import json
        widget = self._makeOne()
        url = 'http://example.com'
        widget.values = url
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
        self.assertEqual(renderer.kw['options'],
                         '{"delay": 400, "minLength": 1}')
        self.assertEqual(renderer.kw['values'],
                         json.dumps(url))

    def test_serialize_iterable(self):
        import json
        widget = self._makeOne()
        vals = [1, 2, 3, 4]
        widget.values = vals
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
        self.assertEqual(renderer.kw['options'],
                         '{"delay": 10, "minLength": 1}')
        self.assertEqual(renderer.kw['values'],
                         json.dumps(vals))

    def test_serialize_not_null_readonly(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct, readonly=True)
        self.assertEqual(renderer.template, widget.readonly_template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)

    def test_serialize_default_display_value(self):
        schema = DummySchema()
        renderer = DummyRenderer()
        field = DummyField(schema, renderer=renderer)
        widget = self._makeOne()
        widget.serialize(field, '1')
        self.assertEqual(renderer.kw['cstruct'], '1')
        self.assertEqual(renderer.kw['visible_cstruct'], '1')

    def test_serialize_custom_display_value(self):
        schema = DummySchema()
        renderer = DummyRenderer()
        field = DummyField(schema, renderer=renderer)
        def display_value(field, cstruct):
            return {'1': 'John Smith'}.get(cstruct)
        widget = self._makeOne(display_value=display_value)
        widget.serialize(field, '1')
        self.assertEqual(renderer.kw['cstruct'], '1')
        self.assertEqual(renderer.kw['visible_cstruct'], 'John Smith')


class DummyRenderer:
    def __call__(self, template, **kw):
        self.template = template
        self.kw = kw


class DummySchema:
    pass


class DummyField:
    def __init__(self, schema=None, renderer=None, name='name'):
        self.schema = schema
        self.renderer = renderer
        self.name = name
