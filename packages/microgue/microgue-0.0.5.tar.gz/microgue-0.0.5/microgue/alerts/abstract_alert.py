import logging
import traceback
from ..services.service import Service

logger = logging.getLogger('microgue')


class SendFailed(Exception):
    pass


class AbstractAlert:
    channel = ''
    icon_emoji = ''
    username = ''
    webhook_url = ''

    def send(self, subject='', message='', add_trace=True):
        logger.debug("########## {} Send ##########".format(self.__class__.__name__))
        logger.debug("message: {}".format(message))

        trace = traceback.format_exc() if add_trace else ''

        data = {
            'text': self._format_alert(subject, message, trace),
            'username': self.username,
            'icon_emoji': self.icon_emoji,
            'unfurl_links': 'true'
        }

        response = Service().request(
            url=self.webhook_url,
            method='POST',
            data=data
        )

        if response.status_code != 200:
            logger.error("########## {} Error".format(self.__class__.__name__))
            logger.error("status_code: {}".format(response.status_code))
            logger.error("data: {}".format(response.data))
            raise SendFailed("Failed ")

        return True

    def _format_alert(self, subject='', message='', trace=''):
        text = "########## {} ##########\n".format(self.__class__.__name__)

        if subject:
            text = text + "########## {}\n".format(subject)

        if message:
            text = text + message + "\n"

        if trace:
            text = text + "########## Traceback\n"
            text = text + trace

        return text
