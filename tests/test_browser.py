import os
import threading
import time

import pytest
import splinter
import waitress

from .demo import app


APP_HTTP_PORT = 65431
APP_URL = f'http://0.0.0.0:{APP_HTTP_PORT}/'
WAIT_DELAY = 0.5

# See .travis.yml to know why we use Chrome by default. You are
# encouraged to also test with `DRIVER_NAME="firefox" pytest` locally.
DRIVER_NAME = os.environ.get('DRIVER_NAME', 'chrome')


class ServerThread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # A better way would be to let the system choose an available
        # port. Passing `port=0` would work but then we would need the
        # child to communicate the port number to the parent process.
        # Let's do something simple instead.
        self.server = waitress.server.create_server(
            app.make_app({}), port=APP_HTTP_PORT, expose_tracebacks=True
        )

    def run(self):
        self.server.run()


@pytest.fixture(scope='module')
def server():
    thread = ServerThread(daemon=True)
    thread.start()
    yield thread.server
    thread.join(0)


@pytest.fixture(scope='module')
def browser(wait_time=2):
    with splinter.Browser(DRIVER_NAME) as b:
        yield b


def find_links(parent, text):
    # `parent.links.find_by_text()` does not return the expected results.
    return [
        link
        for link in parent.find_by_tag('a')
        if link.text == text
    ]


def _check_autocompletion(b, field):
    assert not find_links(b, 'Jimi Hendrix')

    field.fill('jim')
    time.sleep(WAIT_DELAY)
    assert find_links(b, 'Jimi Hendrix')
    assert find_links(b, 'Jimmy Page')

    field.type('i')
    time.sleep(WAIT_DELAY)
    assert find_links(b, 'Jimi Hendrix')
    assert not find_links(b, 'Jimmy Page')

    link = find_links(b, 'Jimi Hendrix')[0]
    link.click()
    assert field.value == 'Jimi Hendrix'


def test_add_form_single(server, browser):  # pylint: disable=redefined-outer-name
    b = browser
    b.visit(APP_URL)

    form = b.find_by_id('add_single').first

    assert not find_links(b, 'Jimi Hendrix')
    field = form.find_by_name('person_autocomplete').first
    _check_autocompletion(b, field)

    save = form.find_by_tag('button').first
    save.click()

    assert '/saved' in b.url
    b.is_text_present('The following data have been saved')
    saved_data = b.find_by_tag('pre').value
    assert saved_data == "{'person': 'jhendrix'}"


def test_add_form_multiple(server, browser):  # pylint: disable=redefined-outer-name
    b = browser
    b.visit(APP_URL)

    form = b.find_by_id('add_multiple').first

    field = form.find_by_name('person_autocomplete').first
    _check_autocompletion(b, field)

    add_person = form.find_by_text('Add Person')
    add_person.click()
    field2 = form.find_by_name('person_autocomplete').last
    assert not find_links(b, 'John Bonham')
    field2.fill('john')
    time.sleep(WAIT_DELAY)
    bonham = find_links(b, 'John Bonham')[0]
    assert bonham
    bonham.click()

    save = form.find_by_tag('button').first
    save.click()

    assert '/saved' in b.url
    b.is_text_present('The following data have been saved')
    saved_data = b.find_by_tag('pre').value
    assert saved_data == "{'persons': ['jhendrix', 'jbonham']}"


def test_edit_form_multiple(server, browser):  # pylint: disable=redefined-outer-name
    b = browser
    b.visit(APP_URL)

    form = b.find_by_id('edit_multiple').first

    fields = form.find_by_name('person_autocomplete')
    field1, field2 = fields.first, fields.last
    assert field1.value == 'Jimmy Page'
    assert field2.value == 'John Bonham'

    field1.fill('jimi')
    time.sleep(WAIT_DELAY)
    hendrix = find_links(b, 'Jimi Hendrix')[0]
    hendrix.click()
    assert field1.value == 'Jimi Hendrix'

    save = form.find_by_tag('button').first
    save.click()

    assert '/saved' in b.url
    b.is_text_present('The following data have been saved')
    saved_data = b.find_by_tag('pre').value
    assert saved_data == "{'persons': ['jhendrix', 'jbonham']}"


def test_read_only_form(server, browser):  # pylint: disable=redefined-outer-name
    b = browser
    b.visit(APP_URL)

    form = b.find_by_id('read_only').first
    inputs = list(form.find_by_tag('input'))
    assert len(inputs) == 1
    assert inputs[0]._element.get_attribute('name') == 'submitted_form'
    paragraphs = list(form.find_by_tag('p'))
    assert len(paragraphs) == 2
    assert paragraphs[0].value == 'Jimmy Page'
    assert paragraphs[1].value == 'John Bonham'
