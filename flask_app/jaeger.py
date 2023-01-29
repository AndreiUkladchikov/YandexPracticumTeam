import functools
import os

import jaeger_client
from config import settings
from flask_opentracing import FlaskTracer
from jaeger_client import Config


def setup_jaeger():
    return Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "enabled": settings.jaeger_tracing,
            "local_agent": {
                "reporting_port": os.environ.get(
                    "JAEGER_AGENT_PORT", jaeger_client.config.DEFAULT_REPORTING_PORT
                ),
                "reporting_host": settings.jaeger_agent_host,
            },
            "logging": settings.jaeger_logging,
        },
        service_name="films-api",
        validate=True,
    ).initialize_tracer()


tracer: FlaskTracer = None


# Decorator
def trace(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        with tracer.start_span(operation_name=fn.__name__) as span:
            return fn(*args, **kwargs)

    return decorated
