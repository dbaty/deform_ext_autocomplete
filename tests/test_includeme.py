import deform
from pkg_resources import resource_filename
from pyramid.config import Configurator

import deform_ext_autocomplete


def test_basics():
    config = Configurator()
    deform_ext_autocomplete.includeme(config)

    search_path = deform.Form.default_renderer.loader.search_path
    our_path = resource_filename('deform_ext_autocomplete', 'templates')
    assert our_path in search_path

    our_registry = deform.Form.default_resource_registry.registry['deform_ext_autocomplete']
    assert None in our_registry
    assert our_registry[None]['css'] == deform_ext_autocomplete.RESOURCES['css']
    assert our_registry[None]['js'] == deform_ext_autocomplete.RESOURCES['js']

    # Checking that we correctly add our static view and include
    # pyramid_chameleon is not easy without digging in the
    # implementation details of Pyramid, and it does not seem worth
    # the hassle.
