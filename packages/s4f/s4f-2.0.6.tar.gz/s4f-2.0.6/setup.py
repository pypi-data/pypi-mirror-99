try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {
    'name': 's4f',
    'version': '2.0.6',
    'author': 'John Lewis',
    'author_email': "john.lewis@takealot.com",
}

setup(**setup_args)