# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import logging

from trytond.pool import Pool
from trytond.config import config
from trytond.transaction import Transaction
from trytond import backend
from trytond.exceptions import LoginException, RateLimitException

import trytond.security_redis as redis

logger = logging.getLogger(__name__)


def _get_pool(dbname):
    database_list = Pool.database_list()
    pool = Pool(dbname)
    if dbname not in database_list:
        pool.init()
    return pool


def config_session_redis():
    return config.get('session', 'redis_uri', default=None)


def config_session_exclusive():
    return config.getboolean('session', 'exclusive', default=True)


def config_session_audit():
    return config.getboolean('session', 'audit', default=True)


def _get_remote_addr(context):
    if context and '_request' in context:
        return context['_request'].get('remote_addr')


def login(dbname, loginname, parameters, cache=True, context=None):
    DatabaseOperationalError = backend.get('DatabaseOperationalError')
    for count in range(config.getint('database', 'retry'), -1, -1):
        with Transaction().start(dbname, 0, context=context) as transaction:
            pool = _get_pool(dbname)
            User = pool.get('res.user')
            try:
                user_id = User.get_login(loginname, parameters)
                break
            except DatabaseOperationalError:
                if count:
                    continue
                raise
            except (LoginException, RateLimitException):
                # Let's store any changes done
                transaction.commit()
                raise
    session = None
    if user_id:
        if not cache:
            session = user_id
        else:
            with Transaction().start(dbname, user_id):
                Session = pool.get('ir.session')
                if config_session_redis():
                    session_key = Session.default_key()
                    if config_session_exclusive():
                        redis.del_sessions(dbname, user_id)
                    redis.set_session(dbname, user_id, session_key, loginname)
                    session = user_id, session_key
                else:
                    session = user_id, Session.new()
        logger.info("login succeeded for '%s' from '%s' on database '%s'",
            loginname, _get_remote_addr(context), dbname)
    else:
        logger.error("login failed for '%s' from '%s' on database '%s'",
            loginname, _get_remote_addr(context), dbname)
    return session


def logout(dbname, user, session, context=None):
    name = None
    if config_session_redis():
        name = redis.get_session(dbname, user, session)
        if name:
            redis.del_session(dbname, user, session)
    else:
        DatabaseOperationalError = backend.get('DatabaseOperationalError')
        for count in range(config.getint('database', 'retry'), -1, -1):
            with Transaction().start(dbname, 0, context=context):
                pool = _get_pool(dbname)
                Session = pool.get('ir.session')
                try:
                    name = Session.remove(session)
                    break
                except DatabaseOperationalError:
                    if count:
                        continue
                    raise
    if name:
        logger.info("logout for '%s' from '%s' on database '%s'",
            name, _get_remote_addr(context), dbname)
    else:
        logger.error("logout failed for '%s' from '%s' on database '%s'",
            user, _get_remote_addr(context), dbname)


def check(dbname, user, session, context=None):
    find = False
    if config_session_redis():
        # check should originally run against config:max_age, we support
        # for now only config:timeout with redis (same as in check_timeout).
        # We don't like the separation into mega session for the bus and
        # normal session for supposedly 'critical' tasks anyway.
        # So it's ok to persist with generally short sessions until there
        # will be really important use of bus messages.
        ttl = redis.hit_session(dbname, user, session)
        if ttl is not None:
            if config_session_audit():
                redis.time_user(dbname, user, ttl)
            find = True
    else:
        DatabaseOperationalError = backend.get('DatabaseOperationalError')
        for count in range(config.getint('database', 'retry'), -1, -1):
            with Transaction().start(
                    dbname, user, context=context) as transaction:
                pool = _get_pool(dbname)
                Session = pool.get('ir.session')
                try:
                    find = Session.check(user, session)
                    break
                except DatabaseOperationalError:
                    if count:
                        continue
                    raise
                finally:
                    transaction.commit()
    if find is None:
        logger.error("session failed for '%s' from '%s' on database '%s'",
            user, _get_remote_addr(context), dbname)
        return
    elif not find:
        logger.info("session expired for '%s' from '%s' on database '%s'",
            user, _get_remote_addr(context), dbname)
        return
    else:
        logger.debug("session valid for '%s' from '%s' on database '%s'",
            user, _get_remote_addr(context), dbname)
        return user


def check_timeout(dbname, user, session, context=None):
    valid = False
    if config_session_redis():
        ttl = redis.hit_session(dbname, user, session)
        if ttl is not None:
            if config_session_audit():
                redis.time_user(dbname, user, ttl)
            valid = True
    else:
        DatabaseOperationalError = backend.get('DatabaseOperationalError')
        for count in range(config.getint('database', 'retry'), -1, -1):
            with Transaction().start(
                    dbname, user, context=context) as transaction:
                pool = _get_pool(dbname)
                Session = pool.get('ir.session')
                try:
                    valid = Session.check_timeout(user, session)
                    break
                except DatabaseOperationalError:
                    if count:
                        continue
                    raise
                finally:
                    transaction.commit()
    if not valid:
        logger.info("session timeout for '%s' from '%s' on database '%s'",
            user, _get_remote_addr(context), dbname)
    return valid


def reset(dbname, session, context={}, user=None):
    if config_session_redis():
        ttl = redis.hit_session(dbname, user, session)
        if ttl is not None and config_session_audit():
            redis.time_user(dbname, user, ttl)
        return
    DatabaseOperationalError = backend.get('DatabaseOperationalError')
    try:
        with Transaction().start(dbname, 0, context=context):
            pool = _get_pool(dbname)
            Session = pool.get('ir.session')
            Session.reset(session)
    except DatabaseOperationalError:
        logger.debug('Reset session failed', exc_info=True)
        pass
