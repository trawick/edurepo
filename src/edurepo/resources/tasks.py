from __future__ import absolute_import

from celery import task
from django.core.management import call_command


@task
def validate():
    call_command('validate_resources')
