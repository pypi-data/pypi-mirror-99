import boto3
import datetime
import logging
import uuid
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Decimal

logger = logging.getLogger('microgue')


class DatabaseConnectionFailed(Exception):
    pass


class ItemAlreadyExists(Exception):
    pass


class DeleteFailed(Exception):
    pass


class AbstractModel:
    table_name = ''

    def __init__(self):
        try:
            database = boto3.resource('dynamodb')
            self.table = database.Table(self.table_name)
        except Exception as e:
            logger.error("########## {} Error".format(self.__class__.__name__))
            logger.error("{}: {}".format(e.__class__.__name__, str(e)))
            raise DatabaseConnectionFailed(str(e))

    def get(self, item_id):
        logger.debug("########## {} Get ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))

        key = Key('id').eq(item_id)
        items = self.table.query(KeyConditionExpression=key).get('Items')
        item = items[0] if items else {}

        logger.debug("return: {}".format(item))

        return self.__replace_decimals(item)

    def insert(self, item):
        item = item.copy()
        logger.debug("########## {} Insert ##########".format(self.__class__.__name__))
        logger.debug("item: {}".format(item))

        if item.get('id') is None:
            item['id'] = str(uuid.uuid4())
        item['created_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.table.put_item(
                Item=item,
                ConditionExpression='attribute_not_exists(id)'
            )
        except Exception as e:
            logger.error("########## {} Insert Error".format(self.__class__.__name__))
            logger.error("{}: {}".format(e.__class__.__name__, str(e)))
            raise ItemAlreadyExists("id ({}) already exists".format(item['id']))

        logger.debug("return: {}".format(item))

        return item

    def update(self, item_id, updated_item):
        logger.debug("########## {} Update ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))
        logger.debug("updated_item: {}".format(updated_item))

        item = self.get(item_id)
        item['updated_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key, value in updated_item.items():
            item[key] = value
        self.table.put_item(Item=item)

        logger.debug("return: {}".format(item))

        return item

    def delete(self, item_id):
        logger.debug("########## {} Delete ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))

        try:
            self.table.delete_item(Key={'id': item_id})
        except Exception as e:
            logger.debug("########## {} Delete Failed".format(self.__class__.__name__))
            logger.debug("{}: {}".format(e.__class__.__name__, str(e)))
            raise DeleteFailed(str(e))

        return True

    def get_all_by_index(self, index, value):
        logger.debug("########## {} - Get All By Index ##########".format(self.__class__.__name__))
        logger.debug("index: {}".format(index))
        logger.debug("value: {}".format(value))

        key = Key(index).eq(value)
        response = self.table.query(IndexName=index + '-index', KeyConditionExpression=key)
        items = response.get('Items')
        while 'LastEvaluatedKey' in response:
            response = self.table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.append(response['Items'])
        return items

    def __replace_decimals(self, item):
        if isinstance(item, list):
            for index in range(len(item)):
                item[index] = self.__replace_decimals(item[index])
            return item
        elif isinstance(item, dict):
            for key in item.keys():
                item[key] = self.__replace_decimals(item[key])
            return item
        elif isinstance(item, Decimal):
            if item % 1 == 0:
                return int(item)
            else:
                return float(item)
        else:
            return item
