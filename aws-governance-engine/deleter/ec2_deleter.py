import boto3
from config import DRY_RUN

def delete_ec2(data):

    for region, instance_id in data.get("ec2_instances", []):
        ec2 = boto3.client("ec2", region_name=region)
        if DRY_RUN:
            print(f"[DRY RUN] Terminate EC2 {instance_id} ({region})")
        else:
            ec2.terminate_instances(InstanceIds=[instance_id])

    for region, vol_id in data.get("ebs_volumes", []):
        ec2 = boto3.client("ec2", region_name=region)
        if DRY_RUN:
            print(f"[DRY RUN] Delete Volume {vol_id}")
        else:
            ec2.delete_volume(VolumeId=vol_id)

    for region, alloc_id in data.get("elastic_ips", []):
        ec2 = boto3.client("ec2", region_name=region)
        if DRY_RUN:
            print(f"[DRY RUN] Release EIP {alloc_id}")
        else:
            ec2.release_address(AllocationId=alloc_id)