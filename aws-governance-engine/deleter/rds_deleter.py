import boto3
from config import DRY_RUN

def delete_rds(data):

    for region, db_id in data:
        rds = boto3.client("rds", region_name=region)
        if DRY_RUN:
            print(f"[DRY RUN] Delete RDS {db_id}")
        else:
            rds.delete_db_instance(
                DBInstanceIdentifier=db_id,
                SkipFinalSnapshot=True
            )