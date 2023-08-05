import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = [req for req in f.read().split('\n') if req]

with open(os.path.join(here, 'requirements-dev.txt')) as f:
    requires_dev = [req for req in f.read().split('\n') if req]

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='molo.commenting',
      version=version,
      description=('Comments helpers for sites built with Molo.'),
      long_description=readme,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt Foundation',
      author_email='dev@praekelt.com',
      url='http://github.com/praekelt/molo.commenting',
      license='BSD',
      keywords='praekelt, mobi, web, django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['molo'],
      install_requires=requires,
      tests_require=requires_dev,
      entry_points={})
