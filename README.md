# Enterprise Cloud Deployment Pipeline (AWS + Terraform + Docker + GitHub Actions)

[![Live Portfolio](https://img.shields.io/badge/Live_Site-portfolio.olinko.co.uk-brightgreen?style=for-the-badge&logo=nginx)](https://portfolio.olinko.co.uk)
[![AWS](https://img.shields.io/badge/AWS-EC2_&_VPC-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)

An automated, production-grade Continuous Integration and Continuous Deployment (CI/CD) pipeline engineered to provision AWS cloud infrastructure via Terraform and deploy containerized microservices automatically upon every `git push`.

---

## Architecture Diagram

```text
  [ Local Workstation ] ─────── ( git push ) ───────► [ GitHub Repository ]
                                                             │
                                                  ( Triggers CI/CD Workflow )
                                                             ▼
                                                  [ GitHub Actions Pipeline ]
                                                  ├─ 1. Code Quality & Tests
                                                  ├─ 2. Build Docker Image
                                                  └─ 3. Push to Docker Hub
                                                             │
                                                  ( Automated SSH Deployment )
                                                             ▼
                                                    [ AWS EC2 Instance ]
  [ User Browser ] ─── ( HTTPS ) ───► [ Nginx Proxy ] ───►  ├─ App Container (Port 8080)
                                    (Let's Encrypt SSL)     └─ Redis Container (Isolated Bridge)
##✨Features & Engineering Highlights

* **Infrastructure as Code (IaC):** Modularized Terraform HCL configurations for dynamic AWS VPC, Subnet, Internet Gateway, and Security Group provisioning.
* **Zero-Touch CI/CD:** End-to-end GitHub Actions workflow automating build, image tagging, registry dispatch to Docker Hub, and live server updates via SSH.
* **Reverse Proxy & SSL Encryption:** Nginx configured to route incoming web traffic (Ports 80/443) seamlessly to internal application containers with automated Let's Encrypt TLS/SSL cert renewals via Certbot.
* **Microservices & Isolated Networking:** Multi-container execution using Docker Compose on an isolated custom Docker bridge network, backed by a persistent Redis NoSQL database instance for real-time visitor tracking.
* **Production Hardening:** Hardened EC2 runtime featuring non-standard SSH access ports, rootless execution, and restrictive AWS Firewall security group ingress policies.

## 🛠️ Tech Stack

| Domain | Technologies |
| :--- | :--- |
| **Cloud Provider** | Amazon Web Services (AWS EC2, VPC, Security Groups, Elastic IP) |
| **Infrastructure as Code** | Terraform |
| **Containers & Orchestration** | Docker, Docker Compose, Docker Hub |
| **CI/CD & Version Control** | GitHub Actions, Git, GitHub |
| **Web Server & Security** | Nginx, Let's Encrypt (Certbot), SSL/TLS, SSH |
| **Application & Database** | Python 3.11, Redis (NoSQL), Bash |

## 🚀 How to Replicate & Deploy

### 1. Clone the Repository
```bash
git clone [https://github.com/Mizan-Olinko/automated-cloud-pipeline.git](https://github.com/Mizan-Olinko/automated-cloud-pipeline.git)
cd automated-cloud-pipeline

### 2. Provision Infrastructure with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

### 3. Deploy Application via GitHub Actions Pipeline

Set the following secrets in your GitHub Repository settings (**Settings > Secrets and variables > Actions**):
* `EC2_HOST` (Your AWS Elastic IP)
* `EC2_USERNAME` (`ubuntu`)
* `EC2_SSH_KEY` (Your private SSH key)
* `DOCKERHUB_USERNAME` & `DOCKERHUB_TOKEN`

Push any commit to the `main` branch to kick off the automated build and deployment:

```bash
git add .
git commit -m "feat: deploy production updates"
git push origin main

## 🌐 Live Verification

Check out the live running application deployment at: **[https://portfolio.olinko.co.uk](https://portfolio.olinko.co.uk)**
