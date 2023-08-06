try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {
    'name': 'tal-service-config',
    'version': '10000001',
    'author': 'John Lewis',
    'author_email': "john.lewis@takealot.com",
}

setup(**setup_args)