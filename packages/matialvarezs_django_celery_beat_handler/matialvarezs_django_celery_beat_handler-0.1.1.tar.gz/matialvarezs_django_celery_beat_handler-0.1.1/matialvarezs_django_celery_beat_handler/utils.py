from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as matialvarezs_django_celery_beat_handler_models
from . import errors as matialvarezs_django_celery_beat_handler_errors
from . import settings
import os, time, random
from django_celery_beat import models as django_celery_beat_models

random_string = "LSbKYbVN5mjMUMXcBcpx40lFNaD1U7DL"

"""
def parse_model_attributes(**kwargs):
	attributes = {}
	
	return attributes

def create_model(**kwargs):

	for key, value in parse_model_attributes(**kwargs).items():
		kwargs[key] = value
	return h_utils.db_create(matialvarezs_django_celery_beat_handler_models.Model, **kwargs)

def get_model(**kwargs):
	return h_utils.db_get(matialvarezs_django_celery_beat_handler_models.Model, **kwargs)

def get_or_none_model(**kwargs):
	return h_utils.db_get_or_none(matialvarezs_django_celery_beat_handler_models.Model, **kwargs)

def filter_model(**kwargs):
	return h_utils.db_filter(matialvarezs_django_celery_beat_handler_models.Model, **kwargs)

def q_model(q, **otions):
	return h_utils.db_q(matialvarezs_django_celery_beat_handler_models.Model, q)

def delete_model(entry, **options):
	return h_utils.db_delete(entry)

def update_model(entry, **kwargs):
	attributes = {}
	for key, value in parse_model_attributes(**kwargs).items():
		attributes[key] = value
	return h_utils.db_update(entry, **attributes)
"""


def filter_periodic_task(**kwargs):
    return h_utils.db_filter(django_celery_beat_models.PeriodicTask, **kwargs)


def get_or_none_periodic_task(**kwargs):
    return h_utils.db_get_or_none(django_celery_beat_models.PeriodicTask, **kwargs)


def create_periodic_task(**kwargs):
    return h_utils.db_create(django_celery_beat_models.PeriodicTask, **kwargs)


def get_or_create_periodic_task(**kwargs):
    return h_utils.db_get_or_create(django_celery_beat_models.PeriodicTask, **kwargs)


def update_periodic_task(periodic_task, **kwargs):
    return h_utils.db_update(periodic_task, **kwargs)


def filter_interval_schedule(**kwargs):
    return h_utils.db_filter(django_celery_beat_models.IntervalSchedule, **kwargs)


def get_or_none_interval_schedule(**kwargs):
    return h_utils.db_get_or_none(django_celery_beat_models.IntervalSchedule, **kwargs)


def create_interval_schedule(**kwargs):
    return h_utils.db_create(django_celery_beat_models.IntervalSchedule, **kwargs)


def get_or_create_interval_schedule(**kwargs):
    return h_utils.db_get_or_create(django_celery_beat_models.IntervalSchedule, **kwargs)


def update_interval_schedule(interval_schedule, **kwargs):
    return h_utils.db_update(interval_schedule, **kwargs)


def filter_crontab_schedule(**kwargs):
    return h_utils.db_filter(django_celery_beat_models.CrontabSchedule, **kwargs)


def get_or_none_crontab_schedule(**kwargs):
    return h_utils.db_get_or_none(django_celery_beat_models.CrontabSchedule, **kwargs)


def create_crontab_schedule(**kwargs):
    return h_utils.db_create(django_celery_beat_models.CrontabSchedule, **kwargs)


def get_or_create_crontab_schedule(**kwargs):
    return h_utils.db_get_or_create(django_celery_beat_models.CrontabSchedule, **kwargs)


def update_crontab_schedule(crontab_schedule, **kwargs):
    return h_utils.db_update(crontab_schedule, **kwargs)
