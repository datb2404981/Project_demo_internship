import pulumi
import pulumi_gcp as gcp
from networking.vpc import vpc 

public1_subnet = gcp.compute.Subnetwork("public1-subnet-dat-intern26",
  network=vpc.id,
  ip_cidr_range="10.0.1.0/24",
  region="asia-east1",
)

public2_subnet = gcp.compute.Subnetwork("public2-subnet-dat-intern26",
  network=vpc.id,
  ip_cidr_range="10.0.2.0/24",
  region="asia-east1",
)

private1_subnet = gcp.compute.Subnetwork("private1-subnet-dat-intern26",
  network=vpc.id,
  ip_cidr_range="10.0.3.0/24",
  region="asia-east1",
  private_ip_google_access=True,
)

private2_subnet = gcp.compute.Subnetwork("private2-subnet-dat-intern26",
  network=vpc.id,
  ip_cidr_range="10.0.4.0/24",
  region="asia-east1",
  private_ip_google_access=True,
)

pulumi.export("public1_subnet", public1_subnet.name)
pulumi.export("public2_subnet", public2_subnet.name)
pulumi.export("private1_subnet", private1_subnet.name)
pulumi.export("private2_subnet", private2_subnet.name)
