# Danh sách các Google Cloud Services đang sử dụng

Dựa trên code Pulumi trong dự án, dưới đây là chi tiết các dịch vụ đang được sử dụng:

## 1. Google Cloud Storage (GCS)
- **Tên Resource:** `bucket-dat-intern26`
- **Loại Resource (Pulumi):** `gcp.storage.Bucket`
- **Vị trí (Location):** `ASIA-EAST1`
- **Cấu hình chi tiết:**
  - **Bảo mật truy cập (Public Access Prevention):** `enforced` (Ngăn chặn hoàn toàn việc truy cập công khai vào bucket, đảm bảo dữ liệu riêng tư).
  - **Quản lý quyền (Uniform Bucket-Level Access):** `true` (Sử dụng thống nhất IAM policies để cấp quyền thay vì dùng Object ACLs cũ).
  - **Bảo vệ chống xóa nhầm (Force Destroy):** `false` (Không cho phép xóa bucket nếu bên trong vẫn còn chứa file, tránh mất dữ liệu).
  - **Cấu hình CORS (Cross-Origin Resource Sharing):** Được thiết lập để cho phép Frontend chạy ở local tương tác với bucket.
    - **Nguồn cho phép (Origin):** `http://localhost:3000`
    - **Phương thức (Methods):** `GET`, `HEAD`, `PUT`, `POST`, `DELETE`
    - **Headers:** `Content-Type`, `Authorization`
    - **Thời gian lưu cache (Max Age):** 3600 giây (1 giờ).

## 2. Virtual Private Cloud (VPC)
- **Tên Resource:** `vpc-dat-intern26`
- **Loại Resource (Pulumi):** `gcp.compute.Network`
- **Cấu hình chi tiết:**
  - **Tạo Subnets tự động (Auto Create Subnetworks):** `false` (Cho phép tự định nghĩa và quản lý các subnets thủ công thay vì dùng dải IP mặc định của Google).

## 3. Subnets (Mạng con)
Dự án sử dụng 4 subnets, tất cả đều nằm trong Region `asia-east1`, thuộc VPC `vpc-dat-intern26`:
- **Public Subnet 1 (`public1-subnet-dat-intern26`):**
  - **Dải IP (CIDR):** `10.0.1.0/24`
- **Public Subnet 2 (`public2-subnet-dat-intern26`):**
  - **Dải IP (CIDR):** `10.0.2.0/24`
- **Private Subnet 1 (`private1-subnet-dat-intern26`):**
  - **Dải IP (CIDR):** `10.0.3.0/24`
  - **Truy cập Google Services riêng (Private IP Google Access):** `true` (Cho phép các máy ảo trong subnet này gọi các dịch vụ của Google mà không cần IP public).
- **Private Subnet 2 (`private2-subnet-dat-intern26`):**
  - **Dải IP (CIDR):** `10.0.4.0/24`
  - **Truy cập Google Services riêng (Private IP Google Access):** `true`

## 4. Cloud Router
- **Tên Resource:** `router-dat-intern26`
- **Loại Resource (Pulumi):** `gcp.compute.Router`
- **Vị trí (Region):** `asia-east1`
- **Chức năng:** Được gắn vào VPC `vpc-dat-intern26`, đóng vai trò định tuyến các luồng traffic cho mạng. Cloud Router là bắt buộc phải có để kết hợp với Cloud NAT, giúp cung cấp luồng traffic outbound.

## 5. Cloud NAT (Network Address Translation)
- **Tên Resource:** `nat-dat-intern26`
- **Loại Resource (Pulumi):** `gcp.compute.RouterNat`
- **Vị trí (Region):** `asia-east1` (gắn vào Router phía trên)
- **Cấu hình chi tiết:**
  - **Cấp phát IP (IP Allocation):** `AUTO_ONLY` (Tự động cấp phát các địa chỉ IP public động cho NAT thay vì phải tự tạo và gán IP tĩnh).
  - **Phạm vi Subnets:** `LIST_OF_SUBNETWORKS` (NAT chỉ áp dụng cho danh sách các subnets cụ thể được chỉ định, không áp dụng cho toàn bộ VPC).
  - **Subnets được áp dụng:** Áp dụng cho các **Private Subnets** với quyền NAT toàn bộ IP (`ALL_IP_RANGES`). Điều này cho phép các máy ảo trong Private Subnets (không có IP Public) có thể truy cập Internet để tải các packages hoặc gọi API bên ngoài, nhưng Internet không thể chủ động kết nối vào trong.
  - **Ghi Log (Logging):** Được bật (`enable=True`) và chỉ ghi lại các lỗi (`filter="ERRORS_ONLY"`) để theo dõi sự cố mà vẫn tiết kiệm chi phí lưu trữ log.

## 6. VPC Firewalls (Tường lửa)
Hệ thống sử dụng 3 bộ quy tắc tường lửa để kiểm soát luồng dữ liệu (traffic):
- **Tường lửa Public Web (`fw-public-web-dat-intern26`):**
  - **Hướng (Direction):** `INGRESS` (Cho phép dữ liệu đi vào)
  - **Nguồn (Source):** Bất kỳ ai trên Internet (`0.0.0.0/0`)
  - **Đích đến (Target):** Các máy ảo có gắn tag `public-web`
  - **Cổng mở (Ports):** Cho phép `TCP` qua cổng `80` (HTTP) và `443` (HTTPS).
- **Tường lửa Private Web (`fw-private-dat-intern26`):**
  - **Hướng (Direction):** `INGRESS` (Cho phép dữ liệu đi vào)
  - **Nguồn (Source):** Chỉ cho phép truy cập từ 2 public subnets (`10.0.1.0/24` và `10.0.2.0/24`)
  - **Đích đến (Target):** Các máy ảo có gắn tag `private-web`
  - **Cổng mở (Ports):** Cho phép `TCP` qua cổng `3000` (App) và `22` (SSH).
- **Tường lửa Private DB (`fw-to-db-dat-intern26`):**
  - **Hướng (Direction):** `INGRESS` (Cho phép dữ liệu đi vào DB)
  - **Nguồn (Source):** Chỉ cho phép truy cập từ 2 private subnets (`10.0.3.0/24` và `10.0.4.0/24`)
  - **Đích đến (Target):** Các máy ảo có gắn tag `private-db` (Database)
  - **Cổng mở (Ports):** Cho phép `TCP` qua cổng `3306` (MySQL).

## 7. Quản lý truy cập (IAM & Service Account)
Dự án áp dụng nguyên tắc phân quyền tối thiểu bằng cách sử dụng các tài nguyên IAM:
- **Service Account (`network-admin-sa`):**
  - **Tên Resource:** `network-sa-dat-intern26`
  - **Chức năng:** Một tài khoản dịch vụ (Service Account) chuyên dụng được tạo ra để cấp quyền thực thi các thao tác liên quan đến mạng.
- **Phân quyền Subnet (Subnetwork IAM):**
  - **Quyền được cấp (Role):** `roles/compute.networkUser` (Người dùng mạng - cho phép tạo tài nguyên máy tính bên trong Subnet).
  - **Đối tượng được cấp (Member):** Service Account `network-admin-sa` ở trên.
  - **Phạm vi áp dụng:** Chỉ được cấp quyền trên 2 **Private Subnets** (`private1_subnet` và `private2_subnet`). Service Account này không có quyền tạo máy ảo trên các public subnets, đảm bảo mức độ bảo mật cao.
