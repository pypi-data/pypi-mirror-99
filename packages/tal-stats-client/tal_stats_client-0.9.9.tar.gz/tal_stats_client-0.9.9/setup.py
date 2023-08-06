try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {
    'name': 'tal_stats_client',
    'version': '0.9.9',
    'author': 'John Lewis',
    'author_email': "john.lewis@takealot.com",
}

setup(**setup_args)