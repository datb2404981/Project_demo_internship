import pulumi
import pulumi_gcp as gcp
from networking.vpc import vpc
import networking.subnets as subnets


network_sa = gcp.serviceaccount.Account("network-sa-dat-intern26",
  account_id="network-admin-sa",
  display_name="Network Admin Service Account",
)

subnet_iam1 = gcp.compute.SubnetworkIAMMember("subnet-iam-dat-intern26",
  subnetwork=subnets.private1_subnet.id,
  role="roles/compute.networkUser",
  member=network_sa.email.apply(lambda email: f"serviceAccount:{email}"),
)

subnet_iam2 = gcp.compute.SubnetworkIAMMember("subnet-iam2-dat-intern26",
  subnetwork=subnets.private2_subnet.id,
  role="roles/compute.networkUser",
  member=network_sa.email.apply(lambda email: f"serviceAccount:{email}"),
)

pulumi.export("network_sa_name", network_sa.name)