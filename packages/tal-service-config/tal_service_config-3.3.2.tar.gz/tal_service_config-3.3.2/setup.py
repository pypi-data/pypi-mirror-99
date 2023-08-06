try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {
    'name': 'tal_service_config',
    'version': '3.3.2',
    'author': 'John Lewis',
    'author_email': "john.lewis@takealot.com",
}

setup(**setup_args)