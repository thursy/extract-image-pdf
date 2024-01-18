import streamlit as st
from io import BytesIO
import ibm_boto3
from ibm_botocore.client import Config, ClientError


def cos_init(creds):
    COS_ENDPOINT = "https://"+creds['endpoint_url_public']

    res = ibm_boto3.resource("s3",
    ibm_api_key_id=creds['COS_APIKEY'],
    ibm_service_instance_id=creds['COS_INSTANCE_CRN'],
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT)

    return res

def get_buckets(res):
    print("Retrieving list of buckets")
    bucket_list = []
    try:
        buckets = res.buckets.all()
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
            bucket_list.append(bucket.name)
        return bucket_list
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))


def get_bucket_contents(bucket_name, res):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    obj_list = []
    try:
        files = res.Bucket(bucket_name).objects.all()
        for file in files:
            file_info = {}
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
            file_info['filename'] = file.key
            file_info['filesize'] = file.size
            obj_list.append(file_info)
        return obj_list
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


def upload_fileobj(bucket_name, item_name, item_bin, res):
    print("Starting upload item to bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        #res.Bucket(bucket_name).upload_file(item_name, item_name)
        res.Bucket(bucket_name).Object(item_name).upload_fileobj(BytesIO(item_bin))
        print("uploaded file: ", item_name)
        return item_name
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def download_file(bucket_name, filename, filename_local, res):
    res.Object(bucket_name, filename).download_file(filename_local)

def upload_file(bucket_name, filename, filename_local, res):
    res.Object(bucket_name, filename).upload_file(filename_local)
