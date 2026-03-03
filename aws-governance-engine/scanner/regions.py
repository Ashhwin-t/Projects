# import boto3

# def get_all_regions():
#     ec2 = boto3.client("ec2", region_name=DEFAULT_REGION)
#     regions = ec2.describe_regions()
#     return [r["RegionName"] for r in regions["Regions"]]

import boto3
from config import DEFAULT_REGION

def get_all_regions():
    ec2 = boto3.client("ec2", region_name=DEFAULT_REGION)
    response = ec2.describe_regions()
    return [region["RegionName"] for region in response["Regions"]]