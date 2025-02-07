Pylgate
============

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: GPLv3 License

PalGate automation using Python.

=================
Table of contents
=================
- `Disclaimer`_

- `Introduction`_

- `Installing`_

- `Usage`_

- `Contributing`_

- `License`_

=======
Disclaimer
=======
This project is intended for research purpose only.

This project is not affiliated with, endorsed by, or in any way officially connected to PalGate.

The use of this software is at the user's own risk. The author(s) of this project take no responsibility and disclaim any liability for any damage, loss, or consequence resulting directly or indirectly from the use or application of this software.

Users are solely responsible for ensuring their use of this project complies with all applicable laws, regulations, and terms of service of any related platforms or services. The author(s) bear no accountability for any actions taken by users of this software.

============
Introduction
============

This project provides a simple way to generate PalGate's derived token, without using third-party libraries!

==========
Installing
==========

Install the package using pip:

.. code-block:: shell

   pip install git+https://github.com/DonutByte/pylgate.git@main

==========
Usage
==========
0. Install the package checkout `Installing`_ for guidance
1. Generate a session token, I have created a `script <examples/generate_linked_device_session_token.py>`_ that acquires a session token using the Device Linking feature, meaning your app will still work
2. Have fun exploring PalGate's API :) - You can checkout `example script <examples/pylgate_usage.py>`_ that verifies the token

============
Contributing
============

Contributions are welcome! Please feel free to submit a Pull Request.

=======
License
=======

This project is licensed under the GNU General Public License v3.0 (GPLv3).

You can find a copy of the license in the LICENSE file or at https://www.gnu.org/licenses/gpl-3.0.en.html.
