import socket

import oneagent
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.engine.base import Connection
import wrapt

from ...log import logger
from ...sdk import sdk


def instrument():
    @event.listens_for(Engine, "before_cursor_execute", named=True)
    def dynatrace_before_cursor_execute(**kw):

        try:
            conn = kw["conn"]
            context = kw["context"]

            statement = kw.get("statement", "")
            db_technology = conn.engine.name
            db_name = conn.engine.url.database

            if not db_name:
                # The connection string might not have a db name
                db_name = "default"

            db_host = conn.engine.url.host
            db_port = conn.engine.url.port

            channel = oneagent.sdk.Channel(oneagent.sdk.ChannelType.OTHER, None)
            if db_host is not None and db_port is not None:
                try:
                    socket.inet_pton(socket.AF_INET6, db_host)
                    db_host = "[{}]".format(db_host)
                except Exception:
                    pass
                channel = oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP, "{}:{}".format(db_host, db_port))

            db_info = sdk.create_database_info(db_name, db_technology, channel)
            tracer = sdk.trace_sql_database_request(db_info, statement)
            logger.debug("Tracing SQLAlchemy: '{}, {}@{}:{}".format(statement, db_name, db_host, db_port))
            tracer.start()
            context.dynatrace_tracer = tracer

        except Exception as e:
            logger.debug("Error instrumenting sqlalchemy: {}".format(e))

    @event.listens_for(Engine, "after_cursor_execute", named=True)
    def dynatrace_after_cursor_execute(**kw):

        try:
            context = kw["context"]

            if context is not None and hasattr(context, "dynatrace_tracer"):
                tracer = context.dynatrace_tracer
                if tracer is not None:
                    # TODO Check if I get stats about query
                    tracer.end()

        except Exception as e:
            logger.debug("Error instrumenting sqlalchemy: {}".format(e))

    @event.listens_for(Engine, "handle_error", named=True)
    def dynatrace_handle_error(**kw):

        try:
            context = kw["exception_context"]

            if context is not None and hasattr(context, "dynatrace_tracer"):
                tracer = context.dynatrace_tracer
                if tracer is not None:
                    logger.debug("Marking purepath as failed")
                    tracer.mark_failed_exc()
                    tracer.end()

        except Exception as e:
            logger.debug("Error instrumenting sqlalchemy: {}".format(e))

    @wrapt.patch_function_wrapper("sqlalchemy.orm.session", "Session.__init__")
    def session_init_dynatrace(wrapped, instance, args, kwargs):
        logger.debug("Tracing sqlalchemy.Session.init")
        with sdk.trace_custom_service("Session.init", "sqlalchemy"):
            return wrapped(*args, **kwargs)

    @wrapt.patch_function_wrapper("sqlalchemy.orm.session", "Session.begin")
    def session_init_dynatrace(wrapped, instance, args, kwargs):
        logger.debug("Tracing sqlalchemy.Session.begin")
        with sdk.trace_custom_service("Session.begin", "sqlalchemy"):
            return wrapped(*args, **kwargs)

    @wrapt.patch_function_wrapper("sqlalchemy.orm.session", "Session.connection")
    def session_init_dynatrace(wrapped, instance, args, kwargs):
        logger.debug("Tracing sqlalchemy.Session.connection")
        with sdk.trace_custom_service("Session.connection", "sqlalchemy"):
            return wrapped(*args, **kwargs)

    @wrapt.patch_function_wrapper("sqlalchemy.orm.session", "Session.close")
    def session_init_dynatrace(wrapped, instance, args, kwargs):
        logger.debug("Tracing sqlalchemy.Session.close")
        with sdk.trace_custom_service("Session.close", "sqlalchemy"):
            return wrapped(*args, **kwargs)

    @wrapt.patch_function_wrapper("sqlalchemy.orm.session", "Session.query")
    def session_init_dynatrace(wrapped, instance, args, kwargs):
        logger.debug("Tracing sqlalchemy.Session.query")
        with sdk.trace_custom_service("Session.query", "sqlalchemy"):
            return wrapped(*args, **kwargs)
