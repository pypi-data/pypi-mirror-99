from distutils.core import setup
import setuptools

setup(
    name='matialvarezs_django_celery_beat_handler',
    packages=['matialvarezs_django_celery_beat_handler'],  # this must be the same as the name above
    version='0.1.2',
    install_requires=[
        'django-ohm2-handlers-light==0.4.1',
        'django-celery-beat==2.2.0'
    ],
    include_package_data=True,
    description='Easy handler django celery beat models: create, filter, get_or_none, get_or_create, update operations',
    author='Matias Alvarez Sabate',
    author_email='matialvarezs@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)