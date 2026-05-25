import pulumi
import pulumi_gcp as gcp
from networking.vpc import vpc 

router = gcp.compute.Router("router-dat-intern26",
  network=vpc.id,
  region="asia-east1",
)

pulumi.export("router_name", router.name)