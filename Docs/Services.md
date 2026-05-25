# Google Cloud Services

## 1. Cloud Storage
- `gcp.storage.Bucket`: **bucket-dat-intern26**
  - Location: `ASIA-EAST1`
  - Public Access Prevention: `enforced`
  - Uniform Bucket Level Access: `True`
  - Force Destroy: `False`
  - CORS: `http://localhost:3000` (GET, HEAD, PUT, POST, DELETE)

## 2. VPC Network
- `gcp.compute.Network`: **vpc-dat-intern26**
  - Auto Create Subnetworks: `False`

## 3. Subnets
- `gcp.compute.Subnetwork`: **public1-subnet-dat-intern26**
  - CIDR: `10.0.1.0/24`
  - Region: `asia-east1`
- `gcp.compute.Subnetwork`: **public2-subnet-dat-intern26**
  - CIDR: `10.0.2.0/24`
  - Region: `asia-east1`
- `gcp.compute.Subnetwork`: **private1-subnet-dat-intern26**
  - CIDR: `10.0.3.0/24`
  - Region: `asia-east1`
  - Private IP Google Access: `True`
- `gcp.compute.Subnetwork`: **private2-subnet-dat-intern26**
  - CIDR: `10.0.4.0/24`
  - Region: `asia-east1`
  - Private IP Google Access: `True`

## 4. Cloud Router & NAT
- `gcp.compute.Router`: **router-dat-intern26**
  - Region: `asia-east1`
  - Network: `vpc-dat-intern26`
- `gcp.compute.RouterNat`: **nat-dat-intern26**
  - Region: `asia-east1`
  - IP Allocate Option: `AUTO_ONLY`
  - Subnetworks: `private1-subnet-dat-intern26`, `private2-subnet-dat-intern26` (ALL_IP_RANGES)

## 5. Firewalls
| Tên Rule | Hướng | Source Ranges | Target Tags | Giao thức | Ports |
|---|---|---|---|---|---|
| `fw-public-web-dat-intern26` | INGRESS | `0.0.0.0/0` | `public-web` | TCP | 80, 443 |
| `fw-private-dat-intern26` | INGRESS | `10.0.1.0/24`, `10.0.2.0/24` | `private-web` | TCP | 3000, 22 |
| `fw-to-db-dat-intern26` | INGRESS | `10.0.3.0/24`, `10.0.4.0/24` | `private-db` | TCP | 3306 |

## 6. IAM & Service Account
- `gcp.serviceaccount.Account`: **network-sa-dat-intern26**
  - Account ID: `network-admin-sa`
- `gcp.compute.SubnetworkIAMMember`: **subnet-iam-dat-intern26**
  - Role: `roles/compute.networkUser`
  - Member: `network-admin-sa`
  - Subnet: `private1-subnet-dat-intern26`
- `gcp.compute.SubnetworkIAMMember`: **subnet-iam2-dat-intern26**
  - Role: `roles/compute.networkUser`
  - Member: `network-admin-sa`
  - Subnet: `private2-subnet-dat-intern26`
