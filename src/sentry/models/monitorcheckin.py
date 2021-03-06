from __future__ import absolute_import, print_function

from django.db import models
from django.utils import timezone

from sentry.db.models import (
    Model,
    BaseManager,
    BoundedPositiveIntegerField,
    EncryptedJsonField,
    FlexibleForeignKey,
    UUIDField,
    sane_repr,
)


class CheckInStatus(object):
    UNKNOWN = 0
    OK = 1
    ERROR = 2
    IN_PROGRESS = 3

    FINISHED_VALUES = (OK, ERROR)

    @classmethod
    def as_choices(cls):
        return (
            (cls.UNKNOWN, 'unknown'),
            (cls.OK, 'success'),
            (cls.ERROR, 'failure'),
            (cls.IN_PROGRESS, 'in_progress'),
        )


class MonitorCheckIn(Model):
    __core__ = True

    guid = UUIDField(unique=True, auto_add=True)
    project_id = BoundedPositiveIntegerField(db_index=True)
    monitor = FlexibleForeignKey('sentry.Monitor')
    location = FlexibleForeignKey('sentry.MonitorLocation', null=True)
    status = BoundedPositiveIntegerField(
        default=0,
        choices=CheckInStatus.as_choices(),
    )
    config = EncryptedJsonField(default=dict)
    duration = BoundedPositiveIntegerField(null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    objects = BaseManager(cache_fields=('guid', ))

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_monitorcheckin'

    __repr__ = sane_repr('guid', 'project_id', 'status')
