from pkg_resources import resource_filename
from unittest.mock import Mock

import deform_ext_autocomplete


def _get_fake_deform_module():
    class FakeDeformModule(object):
        class _Form(object):
            class DefaultRenderer(object):
                class Loader(object):
                    search_path = ('foo', )
                loader = Loader()
            default_renderer = DefaultRenderer()
        Form = _Form()
    return FakeDeformModule()


def test_basics():
    fake_deform = _get_fake_deform_module()
    config = Mock()
    deform_ext_autocomplete.includeme(config, deform=fake_deform)
    search_path = fake_deform.Form.default_renderer.loader.search_path
    assert len(search_path) == 2
    our_path = resource_filename('deform_ext_autocomplete', 'templates')
    assert our_path in search_path
    assert len(config.add_static_view.mock_calls) == 1
    assert config.add_static_view.mock_calls[0][1][1] == 'deform_ext_autocomplete:static'
    assert len(config.include.mock_calls) == 1
    assert config.include.mock_calls[0][1][0] == 'pyramid_chameleon'
