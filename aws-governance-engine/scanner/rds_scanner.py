import boto3
from utils.age_filter import is_old_enough

def scan_rds(region):
    rds = boto3.client("rds", region_name=region)
    data = []

    dbs = rds.describe_db_instances()
    for db in dbs["DBInstances"]:
        if is_old_enough(db["InstanceCreateTime"]):
            data.append((region, db["DBInstanceIdentifier"]))

    return data