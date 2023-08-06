passwheel
=========

A password and secret personal storage tool.

Installation
------------

From PyPI::

    $ pip install passwheel

From the project root directory::

    $ python setup.py install

Usage
-----

commands::

    usage: passwheel [-h] {add,rm,get,dump} ...

    positional arguments:
      {add,rm,get,dump}
        add              add a login
        rm               remove a service or login
        get              fetch creds for service/website
        dump             dump all decrypted credentials

Use ``add`` to add a new service and username to your credentials, and generate
a random password and automatically copy it to the clipboard::

    usage: passwheel add [-h] [--custom] [--words WORDS] [--digits DIGITS]
                         [--symbol]
                         service username

    positional arguments:
      service               service/website
      username              login

    optional arguments:
      --custom, -c          input custom password
      --words WORDS, -w WORDS
                            number of words in generated password
      --digits DIGITS, -d DIGITS
                            number of digits in generated password
      --symbol, -s          append a random symbol to the password

Use ``rm`` to remove a stored password or all passwords for a service::

    usage: passwheel rm [-h] service [username]

    positional arguments:
      service     service/website
      username    login

Use ``get`` to fetch all passwords to a service or website::

    usage: passwheel get [-h] [--copy] service [username]

    positional arguments:
      service     service/website
      username    login name

    optional arguments:
      -h, --help  show this help message and exit
      --copy, -c  copy to clipboard

And finally ``dump`` will dump ALL your usernames and passwords::

    usage: passwheel dump [-h] [--no-passwords] [service]

    positional arguments:
      service             service/website

    optional arguments:
      -h, --help          show this help message and exit
      --no-passwords, -n  dont print passwords

Use --help/-h to view info on the arguments::

    $ passwheel --help

Release Notes
-------------

:0.2.0:
  - Add ``find`` command to use fuzzy string matching
:0.1.2:
  - Add ``changepw`` command to change master password.
:0.1.1:
  - Add mac support for clipboard copying.
  - Add service filter to ``dump``
  - Add username filter and ``--copy`` to ``get`` command
:0.1.0:
  - Project beta release.
:0.0.1:
  - Project created.
