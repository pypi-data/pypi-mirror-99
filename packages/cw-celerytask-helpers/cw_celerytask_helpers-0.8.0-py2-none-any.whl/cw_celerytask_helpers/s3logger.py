"""Helpers for managing logging to S3 in cubicweb-celerytask workers

Add this module 'cw_celerytask_helpers.s3logger' to CELERY_IMPORTS
"""
from __future__ import absolute_import

import os
import logging
from tempfile import TemporaryFile

import boto3
import celery
import six
from celery import signals


@signals.task_prerun.connect
def setup_logging(conf=None, **kwargs):
    bucket = celery.current_app.conf.get('CUBICWEB_CELERYTASK_S3_BUCKET')
    key_pattern = celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_S3_KEY_PATTERN', 'celerytask-%s')
    if not bucket:
        bucket = os.getenv('AWS_S3_BUCKET_NAME')
    if not bucket:
        raise RuntimeError(
            "You asked for S3-based log storage of the task logs "
            "but CUBICWEB_CELERYTASK_S3_BUCKET is not configured. "
            "Please either set CUBICWEB_CELERYTASK_S3_BUCKET in your "
            "celery configuration, or set the AWS_S3_BUCKET_NAME "
            "environment variable.")
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    key = key_pattern % task_id
    handler = S3Handler(level=logging.DEBUG, bucket=bucket, key=key)
    handler.setFormatter(logging.Formatter(
        fmt="%(levelname)s %(asctime)s %(module)s %(process)d %(message)s\n"))
    logger = logging.getLogger('celery.task')
    logger.addHandler(handler)


@signals.task_postrun.connect
def uninstall_logging(conf=None, **kwargs):
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    logger = logging.getLogger('celery.task')
    for handler in logger.handlers:
        if isinstance(handler, S3Handler):
            logger.removeHandler(handler)
            handler.send()


class S3Handler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')
        self.bucket = kwargs.pop('bucket')
        self.closed = False
        self.fobj = TemporaryFile()
        s3_endpoint_url = os.getenv(
            'AWS_S3_ENDPOINT_URL', 'https://s3.amazonaws.com')
        self.s3_cnx = boto3.client('s3', endpoint_url=s3_endpoint_url)
        super(S3Handler, self).__init__(*args, **kwargs)

    def emit(self, record):
        if self.closed or record.task_id in ('???', None):
            return
        formatted = self.format(record)
        if isinstance(formatted, six.text_type):
            self.fobj.write(formatted.encode('utf-8'))
        else:
            self.fobj.write(formatted)

    def send(self):
        self.closed = True
        self.fobj.seek(0)
        self.s3_cnx.upload_fileobj(self.fobj, self.bucket, self.key)
        self.fobj.close()
