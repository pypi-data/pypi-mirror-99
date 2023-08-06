DEPRECATED
==========
This repository is deprecated, for assistance with accessing data please refer to the `data-browser quick start guide. <https://data.humancellatlas.org/guides/quick-start-guide>`_

Data Biosphere Data Store CLI Client
====================================

This repository is a pip-installable command line interface (CLI) and Python library (API) for interacting with the
Data Biosphere Data Storage System (DSS), also called the data store.

Currently the `dbio` package supports interaction with the `data store <https://github.com/DataBiosphere/data-store>`_
for uploading, downloading, and fetching information about data in the data store.

The Data Biosphere CLI is compatible with Python versions 3.5+.

Installation
------------

:code:`pip install dbio-cli`.

Usage
-----

Documentation on readthedocs.io:

* `CLI documentation <https://dbio-cli.readthedocs.io/en/latest/cli.html>`_

* `Python API documentation <https://dbio-cli.readthedocs.io/en/latest/api.html>`_

To see the list of commands you can use, type :code:`dbio --help`.

Configuration management
~~~~~~~~~~~~~~~~~~~~~~~~
The Data Biosphere CLI supports ingesting configuration from a configurable array of sources. Each source is a JSON file.
Configuration sources that follow the first source update the configuration using recursive dictionary merging. Sources
are enumerated in the following order (i.e., in order of increasing priority):

- Site-wide configuration source, ``/etc/dbio/config.json``
- User configuration source, ``~/.config/dbio/config.json``
- Any sources listed in the colon-delimited variable ``DBIO_CONFIG_FILE``
- Command line options

**Array merge operators**: When loading a chain of configuration sources, the Data Biosphere CLI uses recursive
dictionary merging to combine the sources. Additionally, when the original config value is a list, the package
supports array manipulation operators, which let you extend and modify arrays defined in underlying configurations.
See https://github.com/kislyuk/tweak#array-merge-operators for a list of these operators.

Service to Service Authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Google service credentials must be whitelisted before they will authenticate with the Data Biosphere CLI.

Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your Google service credentials file to
authenticate.

One can also use: ``dbio dss login``.

See `Google service credentials <https://cloud.google.com/iam/docs/understanding-service-accounts>`_
for more information about service accounts. Use the `Google Cloud IAM web console
<https://console.cloud.google.com/iam-admin/serviceaccounts>`_ to manage service accounts.

Development
-----------
To develop on the CLI, first run ``pip install -r requirements-dev.txt``. You can install your locally modified copy of
the ``dbio`` package by running ``make install`` in the repository root directory.

To use the command line interface with a local or test DSS, first run ``dbio`` (or ``scripts/dbio`` if you want to use the
package in-place from the repository root directory). This will create the file ``~/.config/dbio/config.json``, which you
can modify to update the value of ``DSSClient.swagger_url`` to point to the URL of the Swagger definition served by your
DSS deployment. Lastly, the CLI enforces HTTPS connection to the DSS API. If you are connecting to a local DSS, make
this change in ``dbio/util/__init__.py`` in the ``SwaggerClient`` object::

    scheme = "http"

To use the Python interface with a local or test DSS, pass the URL of the Swagger definition to the ``DSSClient``
constructor via the ``swagger_url`` parameter::

    client = DSSClient(swagger_url="https://dss.example.com/v1/swagger.json")

You can also layer a minimal config file on top of the default ``config.json`` using the ``DBIO_CONFIG_FILE`` environment
variable, for example::

    export SWAGGER_URL="https://dss.dev.ucsc-cgp-redwood.org/v1/swagger.json"
    jq -n .DSSClient.swagger_url=env.SWAGGER_URL > ~/.config/dbio/config.staging.json
    export DBIO_CONFIG_FILE=~/.config/dbio/config.staging.json

Testing
-------
Before you run tests, first run ``dbio dss login``.  This will open a browser where you can log in to authenticate
with Google. Use an email address from one of the whitelisted domains (in ``DSS_SUBSCRIPTION_AUTHORIZED_DOMAINS_ARRAY``
from `here <https://github.com/DataBiosphere/data-store/blob/master/environment#L55>`_).

Then :code:`make test`.

Primary CI testing is through Travis CI on the
`Gitlab toilspark instance <https://ucsc-ci.org/DataBiosphere/data-store-cli>`_.

Bugs
~~~~
Please report bugs, issues, feature requests, etc. in the
`DataBiosphere/data-store-cli repository on GitHub <https://github.com/DataBiosphere/data-store-cli/issues>`_.


Security Policy
---------------
Please email reports about any security related issues you find to `team-redwood-group@ucsc.edu`.
Use a descriptive subject line for your report email. In addition, please include the following information
along with your report:

* Your name and affiliation (if any).

* A description of the technical details of the vulnerabilities, to help us reproduce your findings.

* An explanation of who can exploit this vulnerability, and what they gain when doing so (an attack scenario).

* Whether this vulnerability is public or known to third parties. If so, please provide details.


License
-------
Licensed under the terms of the `MIT License <https://opensource.org/licenses/MIT>`_.

.. image:: https://api.travis-ci.com/DataBiosphere/data-store-cli.svg?branch=master
        :target: https://travis-ci.com/DataBiosphere/data-store-cli?branch=master
.. image:: https://codecov.io/github/DataBiosphere/data-store-cli/coverage.svg?branch=master
        :target: https://codecov.io/github/DataBiosphere/data-store-cli?branch=master

.. image:: https://img.shields.io/pypi/v/dbio-cli.svg
        :target: https://pypi.python.org/pypi/dbio-cli
.. image:: https://img.shields.io/pypi/l/dbio-cli.svg
        :target: https://pypi.python.org/pypi/dbio-cli
.. image:: https://readthedocs.org/projects/dbio-cli/badge/?version=latest
        :target: https://dbio-cli.readthedocs.io/
