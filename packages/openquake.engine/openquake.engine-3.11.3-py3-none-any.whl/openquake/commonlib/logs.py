# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2010-2021 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.
"""
Set up some system-wide loggers
"""
import os.path
import socket
import logging
from datetime import datetime
from contextlib import contextmanager
from openquake.baselib import zeromq, config, parallel, datastore

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

DBSERVER_PORT = int(os.environ.get('OQ_DBSERVER_PORT') or config.dbserver.port)


def dbcmd(action, *args):
    """
    A dispatcher to the database server.

    :param string action: database action to perform
    :param tuple args: arguments
    """
    host = socket.gethostbyname(config.dbserver.host)
    sock = zeromq.Socket(
        'tcp://%s:%s' % (host, DBSERVER_PORT), zeromq.zmq.REQ, 'connect')
    with sock:
        res = sock.send((action,) + args)
        if isinstance(res, parallel.Result):
            return res.get()
    return res


def touch_log_file(log_file):
    """
    If a log file destination is specified, attempt to open the file in
    'append' mode ('a'). If the specified file is not writable, an
    :exc:`IOError` will be raised.
    """
    open(os.path.abspath(log_file), 'a').close()


def _update_log_record(self, record):
    """
    Massage a log record before emitting it. Intended to be used by the
    custom log handlers defined in this module.
    """
    if not hasattr(record, 'hostname'):
        record.hostname = '-'
    if not hasattr(record, 'job_id'):
        record.job_id = self.job_id


class LogStreamHandler(logging.StreamHandler):
    """
    Log stream handler
    """
    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id

    def emit(self, record):  # pylint: disable=E0202
        _update_log_record(self, record)
        super().emit(record)


class LogFileHandler(logging.FileHandler):
    """
    Log file handler
    """
    def __init__(self, job_id, log_file):
        super().__init__(log_file)
        self.job_id = job_id
        self.log_file = log_file

    def emit(self, record):  # pylint: disable=E0202
        _update_log_record(self, record)
        super().emit(record)


class LogDatabaseHandler(logging.Handler):
    """
    Log stream handler
    """
    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id

    def emit(self, record):  # pylint: disable=E0202
        if record.levelno >= logging.INFO:
            dbcmd('log', self.job_id, datetime.utcnow(), record.levelname,
                  '%s/%s' % (record.processName, record.process),
                  record.getMessage())


@contextmanager
def handle(job_id, log_level='info', log_file=None):
    """
    Context manager adding and removing log handlers.

    :param job_id:
         ID of the current job
    :param log_level:
         one of debug, info, warn, error, critical
    :param log_file:
         log file path (if None, logs on stdout only)
    """
    handlers = [LogDatabaseHandler(job_id)]  # log on db always
    if log_file is None:
        # add a StreamHandler if not already there
        if not any(h for h in logging.root.handlers
                   if isinstance(h, logging.StreamHandler)):
            handlers.append(LogStreamHandler(job_id))
    else:
        handlers.append(LogFileHandler(job_id, log_file))
    for handler in handlers:
        logging.root.addHandler(handler)
    init(job_id, LEVELS.get(log_level, logging.WARNING))
    try:
        yield
    finally:
        for handler in handlers:
            logging.root.removeHandler(handler)


def init(calc_id='nojob', level=logging.INFO):
    """
    1. initialize the root logger (if not already initialized)
    2. set the format of the root handlers (if any)
    3. return a new calculation ID candidate if calc_id is 'job' or 'nojob'
       (with 'nojob' the calculation ID is not stored in the database)
    """
    if not logging.root.handlers:  # first time
        logging.basicConfig(level=level)
    if calc_id == 'job':  # produce a calc_id by creating a job in the db
        calc_id = dbcmd('create_job', datastore.get_datadir())
    elif calc_id == 'nojob':  # produce a calc_id without creating a job
        calc_id = datastore.get_last_calc_id() + 1
    else:
        calc_id = int(calc_id)
        path = os.path.join(datastore.get_datadir(), 'calc_%d.hdf5' % calc_id)
        if os.path.exists(path):
            raise OSError('%s already exists' % path)
    fmt = '[%(asctime)s #{} %(levelname)s] %(message)s'.format(calc_id)
    for handler in logging.root.handlers:
        f = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(f)
    return calc_id
