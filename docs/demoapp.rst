Demonstration application
=========================

``deform_ext_autocomplete`` ships with a demonstration application.
It is located in the ``tests/demo`` directory of the source code. You first
need to install a few things (preferably in a virtual environment, as
usual):

.. code-block:: bash

    $ cd tests/demo
    $ pip install pyramid_chameleon waitress
    $ pip install -e ..

Then run the application:

.. code-block:: bash

    $ python app.py

An HTTP server will start and listen on port 61523 at
`<http://0.0.0.0:61523>`_.
