# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['new_celery_config']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML']

setup_kwargs = {
    'name': 'new-celery-config',
    'version': '0.1.2',
    'description': 'new_celery_config specifies Celery configuration via environment variables.',
    'long_description': '``new_celery_config`` specifies Celery config via environment variables\n=======================================================================\n\n`Celery <https://docs.celeryproject.org/en/stable/>`_ is a distributed task queue library for Python. It accepts some of its configuration via environment variables--but some configuration needs to be specified as Python code.\n\n``new_celery_config`` is a Python package that lets you set any top-level Celery key using an environment variable containing YAML.\n\nInstallation\n------------\n\nThe latest stable can be installed via pip:\n\n.. code:: text\n\n    python3 -m pip install new-celery-config\n\nUsage\n-----\n\n(Usage) as a module\n^^^^^^^^^^^^^^^^^^^\n\nTo set configuration values, you must set an environment variables for each top-level key (`as documented in the Celery documentation <https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration>`_).\n\nEach environment variable is prefixed with ``NEW_CELERY_``, followed by the config key name in lowercase. The value for each environment variable must be valid YAML (or JSON--remember that JSON is a subset of YAML).\n\nYou must also set the environment variable ``CELERY_CONFIG_MODULE`` to ``new_celery_config.as_module`` to enable Celery to read all of the other environment variables that you have set.\n\nFor example, setting these environment variables in the shell looks like:\n\n.. code:: bash\n\n    export CELERY_CONFIG_MODULE=new_celery_config.as_module\n    export NEW_CELERY_broker_url=\'transport://userid:password@hostname:port/virtual_host\'\n    export NEW_CELERY_broker_transport_options=\'{"visibility_timeout": 36000}\'\n\nAnd in your Python code, initialize the Celery object as follows:\n\n.. code:: python\n\n    app = Celery()\n\nIf you want to change the name of the ``CELERY_CONFIG_MODULE``, you can use the ``config_from_envvar`` function. For example:\n\n.. code:: bash\n\n    export ARBITRARY_CELERY_CONFIG_MODULE=new_celery_config.as_module\n\n.. code:: python\n\n    app.config_from_envvar("ARBITRARY_CELERY_CONFIG_MODULE")\n\nYou can test that the configuration works by examining the ``app.conf`` object:\n\n.. code:: python\n\n    print(app.conf.broker_transport_options)\n    # prints out {\'visibility_timeout\': 36000}\n\nUsage (as an object)\n^^^^^^^^^^^^^^^^^^^^\n\nCelery also accepts configuration in the form of a Python object. If you prefer this way, you can give Celery a ``new_celery_config.Config`` object. For example:\n\n.. code:: python\n\n    from celery import Celery\n    import new_celery_config\n\n    app = Celery()\n    app.config_from_object(new_celery_config.Config())\n\n\nContributing changes to ``new_celery_config``\n---------------------------------------------\n\nIf you want to make changes to ``new_celery_config``, you can clone this repository. You can run ``make`` in the root directory to show commands relevant to development.\n\nFor example:\n - ``make fmt`` automatically formats Python code.\n - ``make lint`` runs pylint and mypy to catch errors.\n - ``make test`` runs unit tests.\n',
    'author': 'Neocrym Records Inc.',
    'author_email': 'opensource@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neocrym/new_celery_config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
