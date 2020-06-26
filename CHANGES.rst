Changes
=======

1.0.2 (unreleased)
------------------

- Nothing changed yet.


1.0.1 (2020-06-26)
------------------

- Fix wheel. The wheel for version 1.0 did not include non-Python
  files: templates, CSS and Javascript files were missing.


1.0 (2020-05-27)
----------------

**WARNING :** Brown bag release: the tarball is fine, but the wheel is
 incomplete. Use 1.0.1 instead.

**WARNING :** This release contains many backwards-incompatible changes.

* Define widget requirements so that users can call
  ``Form.get_widget_resources()`` to fetch CSS and JavaScript
  requirements.
* |backward-incompatible| Add ``strip`` parameter that allows to strip
  leading and trailing whitespace on deserialization. As with other
  text-like widgets in Deform, this parameter is now enabled by
  default. This is why this change is not backward compatible.
* Correctly handle ``delay`` parameter.
* |backward-incompatible| Upgrade to Deform 2 and Pyramid 1.10 compatibility
* |backward-incompatible| Bundle a modern version of jqueryUI and upgrade to support it
* |backward-incompatible| Drop Python 2 support in favour of Python 3


0.1 (2012-04-15)
----------------

First public release.


.. role:: raw-html(raw)

.. |backward-incompatible| raw:: html

    <span style="background-color: #ffffbc; padding: 0.3em; font-weight: bold;">backward incompatible</span>
