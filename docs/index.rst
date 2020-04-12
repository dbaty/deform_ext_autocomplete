Extended Autocomplete
=====================

Extended Autocomplete widget provides a few features that are not
available in the default autocomplete widget shipped with `Deform
<http://docs.pylonsproject.org/projects/deform/en/latest/>`_. Essentially,
Extended Autocomplete allows the developer to show a value to the user
that is different from the one that is returned by the widget (and
eventually stored).

For example, let's suppose that we have a database that contains
persons. For each person, the database holds the person's full name
and a unique numerical identifier (a primary key):

=========== ==========
 Identifier Full name
=========== ==========
 1          John Smith
 2          John Smith
 3          Jane Doe
=========== ==========

We need a form that asks us to select a person. This form should
return the person's numerical identifier, which is the piece of
information that uniquely identifies a person.

The default autocomplete widget in Deform shows the value that is
stored. Here, we would either have to show the numerical identifier,
which would obviously be very confusing to the user, or have the form
return the person's full name, which does not match our specification
above.

We would like to let the user select a person by their name, and have
the form return the person's identifier. This is what Extended
Autocomplete proposes.

In fact, three values are handled that may be different:

- the value that is returned by the widget and the form (here, the
  person's numerical identifier);

- the value that appears in a regular text input HTML field once the
  user has selected a person;

- the value that is displayed within the dropdown (the menu that may
  appear when the user starts typing letters in the autocomplete text
  input field). Extended Autocomplete lets us show another value
  here. For example, it could be the name of a person with the typed
  characters highlighted.


Topics
------

.. toctree::
   :maxdepth: 2

   basic.rst
   advanced.rst
   demoapp.rst
   dev.rst
   api.rst
   changes.rst
