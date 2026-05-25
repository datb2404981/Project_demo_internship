import pulumi
import pulumi_gcp as gcp
from networking.router import router
import networking.subnets as subnets

nat = gcp.compute.RouterNat("nat-dat-intern26",
  router=router.name,
  region=router.region,
  nat_ip_allocate_option="AUTO_ONLY",
  source_subnetwork_ip_ranges_to_nat="LIST_OF_SUBNETWORKS",
  subnetworks=[
    gcp.compute.RouterNatSubnetworkArgs(
        name=subnets.private1_subnet.id,
        source_ip_ranges_to_nats=["ALL_IP_RANGES"],
    ),
    gcp.compute.RouterNatSubnetworkArgs(
        name=subnets.private2_subnet.id,
        source_ip_ranges_to_nats=["ALL_IP_RANGES"],
    )
  ],
    log_config=gcp.compute.RouterNatLogConfigArgs(
        enable=True,
        filter="ERRORS_ONLY"
    )
)

pulumi.export("nat_name", nat.name)