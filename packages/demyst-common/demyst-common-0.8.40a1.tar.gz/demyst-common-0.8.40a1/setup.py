from setuptools import setup


setup(
    name='demyst-common',

    version='0.8.40.a1',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',
    packages=['demyst.common'],
    zip_safe=False,

    install_requires=[
        'requests',
        'glom',
        'simplejson',
        'pandas'
    ]
)
