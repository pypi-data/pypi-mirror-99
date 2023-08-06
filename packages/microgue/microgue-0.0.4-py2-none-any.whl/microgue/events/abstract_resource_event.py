import boto3
import json
import logging

logger = logging.getLogger('microgue')


class PublishFailed(Exception):
    pass


class AbstractResourceEvent:
    event_type = ''
    stream_name = ''
    resource_id_field = ''

    def __init__(self):
        self.stream = boto3.client('kinesis')

    def publish(self, before={}, after={}):
        logger.debug("########## {} Publish ##########".format(self.__class__.__name__))
        logger.debug("event_type: {}".format(self.event_type))
        logger.debug("before: {}".format(before))
        logger.debug("after: {}".format(after))
        partition_key = after.get(self.resource_id_field) if after.get(self.resource_id_field, None) is not None else before.get(self.resource_id_field)
        data = {
            'event_type': self.event_type,
            'before': before,
            'after': after
        }

        try:
            self.stream.put_record(
                StreamName=self.stream_name,
                PartitionKey=partition_key,
                Data=json.dumps(data)
            )
        except Exception as e:
            logger.error("########## {} Error".format(self.__class__.__name__))
            logger.error("{}: {}".format(e.__class__.__name__, str(e)))
            raise PublishFailed(str(e))

        return True
