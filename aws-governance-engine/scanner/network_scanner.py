import boto3

def scan_network(region):
    ec2 = boto3.client("ec2", region_name=region)
    elb = boto3.client("elbv2", region_name=region)

    data = {
        "security_groups": [],
        "vpcs": [],
        "subnets": [],
        "nat_gateways": [],
        "load_balancers": []
    }

    for sg in ec2.describe_security_groups()["SecurityGroups"]:
        if sg["GroupName"] != "default":
            data["security_groups"].append((region, sg["GroupId"]))

    for vpc in ec2.describe_vpcs()["Vpcs"]:
        data["vpcs"].append((region, vpc["VpcId"]))

    for subnet in ec2.describe_subnets()["Subnets"]:
        data["subnets"].append((region, subnet["SubnetId"]))

    for nat in ec2.describe_nat_gateways()["NatGateways"]:
        data["nat_gateways"].append((region, nat["NatGatewayId"]))

    lbs = elb.describe_load_balancers()
    for lb in lbs["LoadBalancers"]:
        data["load_balancers"].append((region, lb["LoadBalancerArn"]))

    return data