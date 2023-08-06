# -*- coding: utf-8 -*-


import logging
import datetime
from future.utils import python_2_unicode_compatible

from . import db


@python_2_unicode_compatible
class JobError(Exception):
    """The exception type that jobs raise to signal failure."""

    def __init__(self, message):
        """Initialize a JobError with the given error message string.

        The error message string that you give here will be returned to the
        client site in the job dict's "error" key.

        """
        self.message = message

    def as_dict(self):
        """Return a dictionary representation of this JobError object.

        Returns a dictionary with a "message" key whose value is a string error
        message - suitable for use as the "error" key in a ckanserviceprovider
        job dict.

        """
        return {"message": self.message}

    def __str__(self):
        return self.message


class StoringHandler(logging.Handler):
    '''A handler that stores the logging records
    in the database.'''
    def __init__(self, task_id, input):
        logging.Handler.__init__(self)
        self.task_id = task_id
        self.input = input

    def emit(self, record):
        conn = db.ENGINE.connect()
        try:
            # Turn strings into unicode to stop SQLAlchemy
            # "Unicode type received non-unicode bind param value" warnings.
            message = str(record.getMessage())
            level = str(record.levelname)
            module = str(record.module)
            funcName = str(record.funcName)

            conn.execute(db.LOGS_TABLE.insert().values(
                job_id=self.task_id,
                timestamp=datetime.datetime.now(),
                message=message,
                level=level,
                module=module,
                funcName=funcName,
                lineno=record.lineno))
        finally:
            conn.close()
