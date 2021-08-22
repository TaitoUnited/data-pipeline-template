import io
import os
import sys
import time
import boto3
import json
from minio import Minio
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient
from azure.storage.queue import TextBase64DecodePolicy
from azure.storage.queue import TextBase64EncodePolicy


# Create storage bucket client
def create_storage_bucket_client(
        bucket_name,
        bucket_type=os.environ['STORAGE_TYPE'],
        key1=os.environ['STORAGE_ACCESS_KEY'],
        key2=os.environ['STORAGE_SECRET_KEY'],
        endpoint=os.environ.get('STORAGE_ENDPOINT')):
    if bucket_type == "azure":
        return AzureStorageBucket(bucket_name, key1, key2)

    elif bucket_type == "s3" and not endpoint:
        return S3StorageBucket(bucket_name, key1, key2, endpoint)

    elif bucket_type == "s3" and endpoint:
        return MinioStorageBucket(bucket_name, key1, key2, endpoint)

    else:
        raise Exception("Bucket type not supported: " + bucket_type)


class StorageBucket():

    def __init__(self, bucket_name, key1, key2):
        self.bucket_name = bucket_name
        self.key1 = key1
        self.key2 = key2

    def list_objects(self, file_path_prefix):
        raise Exception("list_objects not implemented")

    def get_object_contents(self, file_path):
        raise Exception("get_object_contents not implemented")

    def listen_changes(
            self,
            file_path_prefix,
            file_path_suffix,
            func,
            queue_name=None):
        raise Exception("listen_changes not implemented")


class AzureStorageBucket(StorageBucket):

    def __init__(self, bucket_name, key1, key2):
        super().__init__(bucket_name, key1, key2)
        self.connect_str = (
            "DefaultEndpointsProtocol=https;AccountName=" +
            key1 +
            ";AccountKey=" +
            key2 +
            ";EndpointSuffix=core.windows.net"
        )
        self.blob_service = BlobServiceClient.from_connection_string(
            self.connect_str
        )
        self.container_client = self.blob_service.get_container_client(
            bucket_name
        )

    def list_objects(self, file_path_prefix):
        objects = []
        blob_list = self.container_client.list_blobs(
            name_starts_with=file_path_prefix
        )
        for blob in blob_list:
            objects.append(blob.name)
        return objects

    def get_object_contents(self, file_path):
        blob_client = self.container_client.get_blob_client(file_path)
        bytes = blob_client.download_blob().readall()
        if bytes is not None:
            return io.BytesIO(bytes)
        return None

    def listen_changes(
            self,
            file_path_prefix,
            file_path_suffix,
            func,
            queue_name=None):

        queue_client = QueueClient.from_connection_string(
            self.connect_str,
            queue_name or self.bucket_name,
            message_encode_policy=TextBase64EncodePolicy(),
            message_decode_policy=TextBase64DecodePolicy()
        )
        # TODO: implement without continuous poll loop
        while True:
            messages = queue_client.receive_messages()
            for message in messages:
                url = None
                try:
                    content = json.loads(message.content)
                    url = content['data']['url']
                    url_split = content['data']['url'].split('/')
                    file_path = '/'.join(url_split[4:])
                    if (
                            not file_path_prefix or
                            file_path.startswith(file_path_prefix)
                        ) and (
                            not file_path_suffix or
                            file_path.endswith(file_path_suffix)
                            ):
                        func(file_path)
                    queue_client.delete_message(
                        message.id,
                        message.pop_receipt
                    )
                except Exception as e:
                    print(
                        "ERROR: Failed to handle storage message for " + url,
                        file=sys.stderr
                    )
                    print(e, file=sys.stderr)
            time.sleep(20)


class S3StorageBucket(StorageBucket):

    def __init__(self, bucket_name, key1, key2, endpoint=None):
        super().__init__(bucket_name, key1, key2)
        self.endpoint = endpoint

        if not endpoint:
            self.client = boto3.client(
                's3',
                aws_access_key_id=key1,
                aws_secret_access_key=key2
            )
        else:
            self.client = boto3.client(
                's3',
                aws_access_key_id=key1,
                aws_secret_access_key=key2,
                endpoint_url="http://" + endpoint,
                use_ssl=False
            )

    def list_objects(self, file_path_prefix):
        objects = []
        response = self.client.list_objects(
            Bucket=self.bucket_name,
            Prefix=file_path_prefix
        )
        if response is not None:
            for obj in response['Contents']:
                objects.append(obj['Key'])
        return objects

    def get_object_contents(self, file_path):
        obj = self.client.get_object(Bucket=self.bucket_name, Key=file_path)
        if obj is not None:
            return obj['Body']
        return None

    def listen_changes(
            self,
            file_path_prefix,
            file_path_suffix,
            func,
            queue_name=None):
        raise Exception("listen_changes not implemented")


class MinioStorageBucket(S3StorageBucket):

    def __init__(self, bucket_name, key1, key2, endpoint):
        super().__init__(bucket_name, key1, key2, endpoint)

    def listen_changes(
            self,
            file_path_prefix,
            file_path_suffix,
            func,
            queue_name=None):
        minio_client = Minio(
            endpoint=self.endpoint,
            access_key=self.key1,
            secret_key=self.key2,
            secure=False
        )
        events = minio_client.listen_bucket_notification(
            self.bucket_name,
            prefix=file_path_prefix,
            suffix=file_path_suffix,
            events=["s3:ObjectCreated:*"]
        )
        for event in events:
            file_path = ''
            try:
                file_path = event['Records'][0]['s3']['object']['key']
                func(file_path)
            except Exception as e:
                print(
                    "ERROR: Failed to handle storage event for " + file_path,
                    file=sys.stderr
                )
                print(e, file=sys.stderr)
