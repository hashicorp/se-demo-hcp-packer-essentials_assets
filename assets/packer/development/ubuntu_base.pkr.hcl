packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.1"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

data "amazon-ami" "ubuntu-server-east" {
  region = var.region
  filters = {
    name                = var.image_name
    root-device-type    = "ebs"
    virtualization-type = "hvm"
  }
  most_recent = true
  owners      = ["099720109477"]
}

source "amazon-ebs" "ubuntu-server-east" {
  region         = var.region
  source_ami     = data.amazon-ami.ubuntu-server-east.id
  instance_type  = "t2.small"
  ssh_username   = "ubuntu"
  ssh_agent_auth = false
  ami_name       = "hashicups-demo-{{timestamp}}_v${var.version}"
  tags           = var.aws_tags
}

build {


  sources = [
    "source.amazon-ebs.ubuntu-server-east"
  ]

  ## HashiCups
  # Add startup script that will run hashicups on instance boot
  provisioner "file" {
    source      = "setup-deps-hashicups.sh"
    destination = "/tmp/setup-deps-hashicups.sh"
  }

  # Move temp files to actual destination
  # Must use this method because their destinations are protected 
  provisioner "shell" {
    inline = [
      "sudo cp /tmp/setup-deps-hashicups.sh /var/lib/cloud/scripts/per-boot/setup-deps-hashicups.sh",
    ]
  }
}