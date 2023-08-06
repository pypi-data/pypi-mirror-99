try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {
    'name': 'tal_kafka',
    'version': '3.0.3',
    'author': 'John Lewis',
    'author_email': "john.lewis@takealot.com",
}

setup(**setup_args)