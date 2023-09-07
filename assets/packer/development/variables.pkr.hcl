variable "region" {
  type    = string
  default = "us-east-2"
}

# This is the version release for this AMI
variable "version" {
  type    = string
  default = "1.0.0"
}

# Canonical publishes Ubuntu images to support numerous features found on EC2.
# https://ubuntu.com/server/docs/cloud-images/amazon-ec2
# The Canonical ID is "099720109477" and we use that in our build section.
# To obtain the whole list of Ubuntu images available use:
# aws ec2 describe-images --owners 099720109477
# But, use filters to make your life a bit easier.

variable "image_name" {
  type    = string
  default = "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*" # changed the image from 18.04 to 20.04
}

# These are meta-data to support document your AMI. 

variable "aws_tags" {
  type = map(string)
  default = {
    "Name"        = "hashicat-ubuntu-us-east-2"
    "Environment" = "Hashicorp Demo"
    "Developer"   = "REPLACE-ME"
    "Owner"       = "development"
    "OS"          = "Ubuntu"
    "Version"     = "Focal 20.04"
  }
}