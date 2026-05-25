import pulumi
import pulumi_gcp as gcp

from networking.vpc import vpc 
import networking.subnets as subnets
import networking.firewall as fw
import networking.iam as iam
import networking.router as router
import networking.nat as nat


bucket = gcp.storage.Bucket("bucket-dat-intern26", 
  location="ASIA-EAST1",
  force_destroy=False,
  public_access_prevention="enforced",
  uniform_bucket_level_access=True,
  cors=[{
    "origin": ["http://localhost:3000"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "responseHeader": ["Content-Type", "Authorization"],
    "maxAgeSeconds": 3600
}])

pulumi.export("bucket_name", bucket.name)
pulumi.export("bucket_url", bucket.url)

