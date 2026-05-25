import pulumi 
import  pulumi_gcp as gcp
from networking.vpc import vpc
from networking.subnets import private1_subnet

vm_service_account = gcp.serviceaccount.Account("vm-dat-intern26",
    account_id="ai-vm-dat-intern26",
    display_name="Service Account for AI VM"
)

setup_script ="""
#!/bin/bash
echo "Đang khởi tạo môi trường máy chủ..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs git
echo "Môi trường đã sẵn sàng!" > /var/log/vm_setup.log
"""

health_check = gcp.compute.HealthCheck("backend-health-check",
    check_interval_sec=5,
    timeout_sec=5,
    healthy_threshold=2,
    unhealthy_threshold=2,
    http_health_check=gcp.compute.HealthCheckHttpHealthCheckArgs(
        port=3000, 
        request_path="/" 
    )
)

gce_template = gcp.compute.InstanceTemplate("gce-template-dat-intern26",
    machine_type="e2-small",
    region="asia-east1",
    disks=[gcp.compute.InstanceTemplateDiskArgs(
        source_image="debian-cloud/debian-11",
        disk_size_gb=20,
        disk_type="pd-ssd",
        boot=True,
        auto_delete=True,
    )],
    network_interfaces=[{
        "network": vpc.id,
        "subnetwork": private1_subnet.id
    }],
    metadata={
        "startup-script": setup_script
    },
    service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
        email=vm_service_account.email,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    ),
    tags=["private-web"]
)

mig=gcp.compute.InstanceGroupManager("mig-dat-intern26",
    base_instance_name="node-backend-mig",
    versions=[{
        "instance_template": gce_template.id,
    }],
    zone="asia-east1-a",
    auto_healing_policies={
        "health_check": health_check.id,
        "initial_delay_sec": 300
    },
    target_size=1,
)

autoscaler = gcp.compute.Autoscaler("autoscaler-dat-intern26",
    target=mig.id,
    zone="asia-east1-a",
    autoscaling_policy={
        "min_replicas": 1,
        "max_replicas": 3,
        "cooldown_period": 60,
        "cpu_utilization": {
            "target": 0.8
        }
    },
)

pulumi.export("mig_name", mig.name)
pulumi.export("autoscaler_name", autoscaler.name)