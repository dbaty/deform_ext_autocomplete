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
        pstruct = {'person': '', 'person_autocomplete': ''}
        self.assertEqual(widget.deserialize(field, pstruct), colander.null)

    def test_deserialize_filled(self):
        schema = DummySchema()
        field = DummyField(schema, name='person')
        widget = self._makeOne()
        pstruct = {'person': 'jsmith', 'person_autocomplete': 'John Smith'}
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
        url='http://example.com'
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
                         '{"delay": 400, "minLength": 2}')
        self.assertEqual(renderer.kw['values'],
                         json.dumps(url))

    def test_serialize_iterable(self):
        import json
        widget = self._makeOne()
        vals = [1,2,3,4]
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
                         '{"delay": 10, "minLength": 2}')
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


class TestIncludeMe(TestCase):

    def _call_fut(self, config, fake_deform):
        from deform_ext_autocomplete import includeme
        return includeme(config, fake_deform)

    def _get_fake_deform_module(self):
        class FakeDeformModule(object):
            class _Form(object):
                class DefaultRenderer(object):
                    class Loader(object):
                        search_path = ('foo', )
                    loader = Loader()
                default_renderer = DefaultRenderer()
            Form = _Form()
        return FakeDeformModule()

    def test_basics(self):
        from pkg_resources import resource_filename
        fake_deform = self._get_fake_deform_module()
        config = 'fake'
        self._call_fut(config, fake_deform=fake_deform)
        search_path = fake_deform.Form.default_renderer.loader.search_path
        self.assertTrue(len(search_path) == 2)
        our_path = resource_filename('deform_ext_autocomplete', 'templates')
        self.assertIn(our_path, search_path)


class DummyRenderer(object):
    def __call__(self, template, **kw):
        self.template = template
        self.kw = kw


class DummySchema(object):
    pass


class DummyField(object):
    def __init__(self, schema=None, renderer=None, name='name'):
        self.schema = schema
        self.renderer = renderer
        self.name = name
