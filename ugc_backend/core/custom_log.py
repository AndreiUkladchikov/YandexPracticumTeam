import logstash
import loguru

from core.config import settings

logger = loguru.logger
logger.add(
    logstash.LogstashHandler(settings.logstash_host, settings.logstash_port, version=1)
)
