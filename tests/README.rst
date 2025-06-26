==============
Testing pylgate
==============

pylgate uses `pytest <https://docs.pytest.org/en/stable/>`_ for testing. To run tests on your own you'll need to:

1. Install dependencies required for testing

.. code-block:: shell

    # In project's root directory
    pip install . --group tests

2. Have a valid *session token*. If you don't have one refer to ``Generate a Session Token`` section in the root directory ``README.rst``

Terminology
^^^^^^^^^^^

In the context of the ``tests`` directory, "*gate*" corresponds to what the PalGate API refers to as "*device*".
This terminology is used to distinguish it from the *device-linking* feature, which is explained on PalGate's website as:
    This function [device linking] allows the PalGate app to be used on a tablet or in-car multimedia system without a SIM card or phone number for registration, using the same user account with the exact same gates.

Running Tests
=============

Tests interact with PalGate's API, therefore you'll need to supply it with a *session token*, *phone number*, *token type* as following:

.. code-block:: shell

    pytest -m "not causes_side_effects" --session-token=<session token> --phone-number=<phone number> --token-type={0,1,2}

The ``-m "not causes_side_effects"`` is there to run tests which do not have side-effects (other than reaching over the Internet to PalGate's API)

..................

Test with side-effects:

``test_gate_open``
    Opens the first non-local-only gate from account's list of gates

``test_device_linking``
    Overrides the second (``TokenType.SECONDARY``) linked device

..................

If you wish to run all tests **including those with side-effects** use the command bellow:

.. code-block:: shell

    pytest --session-token=<session token> --phone-number=<phone number> --token-type={0,1,2}
