import boto3
from utils.age_filter import is_old_enough

def scan_ec2(region):
    ec2 = boto3.client("ec2", region_name=region)

    data = {
        "ec2_instances": [],
        "ebs_volumes": [],
        "elastic_ips": []
    }

    # EC2
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for res in page["Reservations"]:
            for instance in res["Instances"]:
                if is_old_enough(instance["LaunchTime"]):
                    data["ec2_instances"].append((region, instance["InstanceId"]))

    # Unattached volumes
    volumes = ec2.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )
    for vol in volumes["Volumes"]:
        if is_old_enough(vol["CreateTime"]):
            data["ebs_volumes"].append((region, vol["VolumeId"]))

    # Unattached EIP
    addresses = ec2.describe_addresses()
    for addr in addresses["Addresses"]:
        if "InstanceId" not in addr:
            data["elastic_ips"].append((region, addr["AllocationId"]))

    return data