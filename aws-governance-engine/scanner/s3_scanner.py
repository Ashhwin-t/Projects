import boto3
from datetime import datetime, timezone
from config import AGE_THRESHOLD_DAYS

def scan_s3():
    s3 = boto3.client("s3")
    buckets_to_delete = []

    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        if AGE_THRESHOLD_DAYS == 0:
            buckets_to_delete.append(bucket["Name"])
        else:
            age = (datetime.now(timezone.utc) - bucket["CreationDate"]).days
            if age >= AGE_THRESHOLD_DAYS:
                buckets_to_delete.append(bucket["Name"])

    return buckets_to_delete