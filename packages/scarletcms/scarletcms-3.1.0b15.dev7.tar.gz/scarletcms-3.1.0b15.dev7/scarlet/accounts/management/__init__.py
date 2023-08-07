from django import VERSION as DJANGO_VERSION
from django.contrib import auth
from django.contrib.auth import models as auth_app
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate

from .. import settings


def ensure_groups_sync(app, created_models, verbosity, **kwargs):
    for group in settings.BASE_GROUPS:
        Group.objects.get_or_create(name=group)


def ensure_groups(sender=None, **kwargs):
    for group in settings.BASE_GROUPS:
        Group.objects.get_or_create(name=group)


post_migrate.connect(ensure_groups, sender=auth_app, dispatch_uid="ensure_groups")
