import pulumi
import pulumi_gcp as gcp

vpc = gcp.compute.Network("vpc-dat-intern26",
  auto_create_subnetworks=False
)

pulumi.export("vpc_name", vpc.name)