import boto3
from config import DRY_RUN

def delete_s3(buckets):

    s3 = boto3.resource("s3")

    for bucket_name in buckets:
        bucket = s3.Bucket(bucket_name)

        if DRY_RUN:
            print(f"[DRY RUN] Delete S3 bucket {bucket_name}")
        else:
            bucket.objects.all().delete()
            bucket.delete()