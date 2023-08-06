from setuptools import setup, find_packages

setup(
    name='django-csv-tool',
    version='0.3.10',
    author='John Leith',
    author_email='leith.john@gmail.com',
    packages=find_packages(),
    url='https://bitbucket.org/freakypie/django-csv-tool',
    description='Tool to help create CSV imports faster',
    install_requires=[
        'six'
    ]
)
