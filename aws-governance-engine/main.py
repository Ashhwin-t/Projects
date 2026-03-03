from scanner.regions import get_all_regions
from scanner.ec2_scanner import scan_ec2
from scanner.rds_scanner import scan_rds
from scanner.s3_scanner import scan_s3
from scanner.network_scanner import scan_network

from classifier.classifier import classify_resources

from deleter.ec2_deleter import delete_ec2
from deleter.rds_deleter import delete_rds
from deleter.s3_deleter import delete_s3
from deleter.network_deleter import delete_network

from config import DRY_RUN

def main():

    regions = get_all_regions()

    scanned = {
        "ec2_instances": [],
        "ebs_volumes": [],
        "elastic_ips": [],
        "rds_instances": [],
        "s3_buckets": [],
        "security_groups": [],
        "vpcs": [],
        "subnets": [],
        "nat_gateways": [],
        "load_balancers": []
    }

    print("\nScanning all AWS regions...\n")

    for region in regions:
        ec2_data = scan_ec2(region)
        net_data = scan_network(region)
        rds_data = scan_rds(region)

        for k in ec2_data:
            scanned[k].extend(ec2_data[k])

        for k in net_data:
            scanned[k].extend(net_data[k])

        scanned["rds_instances"].extend(rds_data)

    scanned["s3_buckets"] = scan_s3()

    billable, non_billable = classify_resources(scanned)

    print("\n================ BILLABLE RESOURCES ================\n")
    for svc, items in billable.items():
        print(f"{svc}: {len(items)}")

    print("\n================ NON-BILLABLE RESOURCES ================\n")
    for svc, items in non_billable.items():
        print(f"{svc}: {len(items)}")

    print("\nDRY RUN:", DRY_RUN)

    if input("\nDelete BILLABLE resources? (yes/no): ").lower() == "yes":
        delete_ec2(billable)
        delete_rds(billable.get("rds_instances", []))
        delete_s3(billable.get("s3_buckets", []))

    if input("\nDelete NON-BILLABLE resources? (yes/no): ").lower() == "yes":
        delete_network(non_billable)

    print("\nProcess Completed.")

if __name__ == "__main__":
    main()