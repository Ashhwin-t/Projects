def classify_resources(scanned_data):

    billable_services = [
        "ec2_instances",
        "ebs_volumes",
        "elastic_ips",
        "rds_instances",
        "nat_gateways",
        "load_balancers",
        "s3_buckets"
    ]

    billable = {}
    non_billable = {}

    for service, items in scanned_data.items():
        if service in billable_services:
            billable[service] = items
        else:
            non_billable[service] = items

    return billable, non_billable