#!/bin/bash
set -e

export DEBIAN_FRONTEND=noninteractive
export TZ=America/Toronto

# Install necessary dependencies
sudo apt-get update
sudo apt-get -y install git docker.io unzip auditd

# Install latest version of docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Get HashiCups config
git clone https://github.com/hashicorp-demoapp/hashicups-setups
cd hashicups-setups/docker-compose-deployment
git checkout server

# Changing the default entry point password for DB to avoid
# default password in config file.
 RANDOM_PASSWORD=$(openssl rand -hex 20)
 sudo sed -i "s/=password/=$RANDOM_PASSWORD/g" docker-compose.yaml
 sudo sed -i "s/=password/=$RANDOM_PASSWORD/g" conf.json
 unset RANDOM_PASSWORD

# Start HashiCups in background
sudo docker-compose up -d