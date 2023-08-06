# Python 2.7/3.8 module to manage the SomConnexio's ERP integration with OTRS

This library manages all the business logic between the Som Connexio's systems and the ticketing tool OTRS.

## [Processes](https://gitlab.com/coopdevs/otrs-somconnexio/-/wikis/processes/README)

## OTRS Configuration

Configure the web services in OTRS:

#### Ticket Connector (Provider)

* Usage:
It exposes the Ticket, Article and DynamicFields object and allows to get, create, update and remove tickets. We use the PyOTRS to interact with it. Look in the [PyOTRS](https://gitlab.com/rhab/PyOTRS/-/blob/master/README.rst) docs for more info.

* Configuration:
Use the template provided by the PyOTRS client: https://gitlab.com/rhab/PyOTRS/-/blob/master/webservices_templates/GenericTicketConnectorREST.yml

#### CustomerUser Connector (Provider)

* Usage:
It's a RPCConnector. It interacts with the OTRS objects directly calling the class methods.

* Configuration:
You need admin permissions to manage it.
Contact with your OTRS provider.

#### MMCaller Connector (Requester)

* Usage:
It calls MMProxy when an event is raised.

* Configuration:
https://gitlab.com/coopdevs/somconnexio-documentation/-/blob/master/integracions/masmovil.md#webservice-dotrs

## Environment configuration

### OTRSClient

The client to interact with OTRS. You need to define the next environment variables to use the client:

```
OTRS_URL=       # Baseurl of the OTRS instance
OTRS_USER=      # Creadencials of user with write acces to OTRS
OTRS_PASSW=
```

## Python version

We are using [Pyenv](https://github.com/pyenv/pyenv) to fix the Python version and the virtualenv to test the package.

You need:

* Intall and configure [`pyenv`](https://github.com/pyenv/pyenv)
* Install and configure [`pyenv-virtualenvwrapper`](https://github.com/pyenv/pyenv-virtualenvwrapper)
* Intall locally the version of python needed:

```
$ pyenv install 3.8.2
```

* Create the virtualenv to use:

```
$ pyenv virtualenv 3.8.2 otrs_somconnexio
```


## Python packages requirements

Install the Python packages in the virtual environment:

```
$ pyenv exec pip install -r requirements.txt
```

## Run tests

To run the test you can run:

```
$ tox
```

Also you can run only the tests running:

```
$ python setup.py test
```

If running the tests with tox, they will be tested with both python3.8 and python2.7. This is because OTRS-SomConnexio works with an ERP which uses python2, as well as with other packages that use python3.
