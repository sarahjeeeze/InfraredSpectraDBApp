import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'bcrypt',
    'requests',
    'cryptography',
    'deform',
    'docutils',
    'alembic',
    'matplotlib',
    'plaster_pastedeploy',
    'pyramid >= 1.9',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'pymysql',
    'jcamp',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'ColanderAlchemy',
    'pathlib',
    
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='ftirdb',
    version='0.0',
    description='ftirdb',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = ftirdb:main',
        ],
        'console_scripts': [
            'initialize_ftirdb_db = ftirdb.scripts.initialize_db:main',
        ],
    },
)
