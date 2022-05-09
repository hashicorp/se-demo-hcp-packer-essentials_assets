variable "cidr_vpc" {
  description = "CIDR block for the VPC"
  default     = "10.1.0.0/16"
}
variable "cidr_subnet" {
  description = "CIDR block for the subnet"
  default     = "10.1.0.0/24"
}

variable "environment_tag" {
  description = "Environment tag"
  default     = "HashiCups Frontend Production"
}

variable "region" {
  description = "The region Terraform deploys the new instance"
  default     = "us-east-2"
}

variable "hcp_bucket_ubuntu" {
  description = "The Bucket where our AMI is listed."
  default     = "hashicups-frontend-ubuntu"
}

variable "hcp_channel" {
  description = "HCP Packer channel name"
  default     = "hashicups-development"
}



