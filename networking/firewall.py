import pulumi
import pulumi_gcp as gcp
from networking.vpc import vpc


fw_public_web =  gcp.compute.Firewall("fw-public-web-dat-intern26",
    network=vpc.id,
    direction="INGRESS",
    priority=1000,
    allows=[{
        "protocol": "tcp",
        "ports": ["80", "443"],
    }],
    source_ranges=["0.0.0.0/0"],
    target_tags=["public-web"],
)

fw_private_web = gcp.compute.Firewall("fw-private-dat-intern26",
    network=vpc.id,
    direction="INGRESS",
    priority=1000,
    allows=[{
        "protocol": "tcp",
        "ports": ["3000", "22"],
    }],
    source_ranges=["10.0.1.0/24", "10.0.2.0/24"],
    target_tags=["private-web"],
)

fw_to_db = gcp.compute.Firewall("fw-to-db-dat-intern26",
    network=vpc.id,
    direction="INGRESS",
    priority=1000,
    allows=[{
        "protocol": "tcp",
        "ports": ["3306"],
    }],
    source_ranges=["10.0.3.0/24", "10.0.4.0/24"],
    target_tags=["private-db"],
)

pulumi.export("fw_public_web", fw_public_web.name)
pulumi.export("fw_private_web", fw_private_web.name)
pulumi.export("fw_to_db", fw_to_db.name)