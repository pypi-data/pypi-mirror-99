from setuptools import setup

setup(
    name='salure_helpers',
    version='12.3.4',
    description='Files with helpful code, developed by Salure',
    url='https://bitbucket.org/salurebi/salure_helpers/',
    author='Salure',
    author_email='bi@salure.nl',
    license='Salure License',
    packages=['salure_helpers'],
    package_data={'salure_helpers': ['templates/*', 'datasets/*', 'helpers/*']},
    install_requires=[
        'aiohttp>=3,<4',
        'pandas>=1,<1.2',
        'mandrill-really-maintained>=1,<2',
        'numpy>=1,<1.20',
        'pymysql>=1,<2',
        'requests>=2,<3',
        'pysftp>=0,<1',
        'pyarrow>=0,<3',
        'twine>=3,<4',
        'clickhouse-driver>=0,<1',
        'fs>=2,<3',
        'python-gnupg>=0,<1',
        'xmltodict>=0,<1',
        'zeep>=4,<5'
    ],
    zip_safe=False
)
