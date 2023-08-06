import logging
from .secrets import Secrets

logging.basicConfig()
logger = logging.getLogger('microgue')
logger.setLevel(logging.CRITICAL)


class SecretsWithoutLogging(Secrets):
    pass
