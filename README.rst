.. 

cloud
======================

Quickstart
----------

To bootstrap the project::

    virtualenv cloud
    source cloud/bin/activate
    cd path/to/cloud/repository
    pip install -r requirements.txt
    pip install -e .
    cp cloud/settings/local.py.example cloud/settings/local.py
    manage.py syncdb

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.

Contributing
------------

Please do. Just start an Issue ticket with your idea or open a Pull Request!

License
-------

GPLv3

Authors
-------

Juan Carlos Ferrer @juancferrer and other contributors
