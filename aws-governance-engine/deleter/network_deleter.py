import boto3
from config import DRY_RUN

def delete_network(data):

    for region, sg in data.get("security_groups", []):
        ec2 = boto3.client("ec2", region_name=region)
        if DRY_RUN:
            print(f"[DRY RUN] Delete SG {sg}")
        else:
            try:
                ec2.delete_security_group(GroupId=sg)
            except:
                pass