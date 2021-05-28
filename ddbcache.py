import boto3
import os
import time
from botocore.exceptions import ClientError


class DDBCache(object):
    def __init__(self, table_name: str):
        self._sess = boto3.Session()
        ddb = self._sess.resource('dynamodb', region_name=os.environ.get("AWS_REGION"))
        self._table = ddb.Table(table_name)

    def get(self, repo_slug: str):
        try:
            resp = self._table.get_item(Key={'repoSlug': repo_slug})
            if 'Item' not in resp:
                return None
            # Return None if we're beyond TTL limits, so that we can re-populate the item.
            if int(time.time()) > resp['Item']['ttl']:
                return None
            return resp['Item']
        except ClientError as e:
            print(e.response['Error']['Message'])

    def put(self, repo_slug: str, data: any):
        try:
            resp = self._table.update_item(
                Key={
                    'repoSlug': repo_slug
                },
                UpdateExpression="set #ts = :ts, repodata = :repodata",
                ExpressionAttributeValues={
                    ':ts': int(time.time()) + 300,
                    ':repodata': data
                },
                ExpressionAttributeNames={
                    '#ts': 'ttl'
                }
            )
            return resp
        except ClientError as e:
            print("ERR: ", e)
