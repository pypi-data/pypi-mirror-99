# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyramid_autowire']

package_data = \
{'': ['*']}

install_requires = \
['pyramid>=1.5', 'typing-extensions>=3.7.4,<4.0.0', 'zope.interface']

setup_kwargs = {
    'name': 'pyramid-autowire',
    'version': '0.1.0.dev3',
    'description': 'Dependency injection for pyramid views',
    'long_description': "====================\n``pyramid_autowire``\n====================\n\n``pyramid_autowire`` is a package that allows your pyramid views to use pyramids registry for dependency injection.\n\n.. code-block:: python\n\n    from pyramid_autowire import autowired\n\n    @view_defaults(route_name='test_route', mapper=autowired)\n    class Posts:\n        def __init__(\n            # Standard pyramid (context, request) and (request,) arguments\n            # are available through position-only args\n            self, request, /,\n            # the database and user objects will be injected from the registry\n            database: IDatabase, active_user: IUser\n        ):\n            self.request = request\n            self.database = database\n            self.active_user = active_user\n    \n        @view_config()\n        def view_post(\n            self, *,\n            # the matchdict is injected as keyword-only args\n            post_id\n        ):\n            return self.database.query(Post, post_id)\n    \n    def includeme(config):\n        registry = config.registry\n\n        # pretend for the example that the database session is global\n        registry.registerUtility(MyDatabase(), IDatabase)\n\n        def get_active_user(request):\n            # Fetch active user from the request data\n            ...\n\n        registry.registerAdapter(get_active_user, (IRequest, ), IUser)\n",
    'author': 'Nick Beeuwsaert',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickBeeuwsaert/pyramid_autowire',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
