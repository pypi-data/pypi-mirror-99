mautrix-python
==============

|PyPI| |Python versions| |License|

A Python 3.7+ asyncio Matrix framework.

Matrix room: `#maunium:maunium.net`_

Sponsors
--------
* `kumitterer`_


.. _kumitterer: https://kumi.website/


Components
----------

* Basic HTTP request sender (mautrix.api_)

* `Client API`_ endpoints as functions (mautrix.client.api_)

* Medium-level application service framework (mautrix.appservice_)

  * Basic transaction and user/alias query support (based on Cadair's python-appservice-framework_)
  * Basic room state storage
  * Intent wrapper around the client API functions (design based on matrix-appservice-bridge)

* Medium-level end-to-end encryption framework (mautrix.crypto_)

  * Handles all the complicated e2ee key exchange

* High-level bridging utility framework (mautrix.bridge_)

  * Base class for bridges
  * Common bridge configuration and appservice registration generation things
  * Double-puppeting helper
  * End-to-bridge encryption helper

* High-level client framework (mautrix.client_)

  * Syncing and event handling helper.
  * End-to-end encryption helper.

.. _#maunium:maunium.net: https://matrix.to/#/#maunium:maunium.net
.. _python-appservice-framework: https://github.com/Cadair/python-appservice-framework/
.. _Client API: https://matrix.org/docs/spec/client_server/r0.6.1.html

.. _mautrix.api: https://mautrix.readthedocs.io/en/latest/mautrix.api.html
.. _mautrix.client.api: https://mautrix.readthedocs.io/en/latest/mautrix.client.api.html
.. _mautrix.appservice: https://mautrix.readthedocs.io/en/latest/mautrix.appservice.html
.. _mautrix.bridge: https://mautrix.readthedocs.io/en/latest/mautrix.bridge.html
.. _mautrix.client: https://mautrix.readthedocs.io/en/latest/mautrix.client.html
.. _mautrix.crypto: https://mautrix.readthedocs.io/en/latest/mautrix.crypto.html

.. |PyPI| image:: https://img.shields.io/pypi/v/mautrix.svg
   :target: https://pypi.python.org/pypi/mautrix
.. |ReadTheDocs| image:: https://img.shields.io/readthedocs/mautrix.svg
   :target: https://mautrix.readthedocs.io
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/mautrix.svg
.. |License| image:: https://img.shields.io/github/license/tulir/mautrix-python.svg
   :target: https://github.com/tulir/mautrix-python/blob/master/LICENSE
