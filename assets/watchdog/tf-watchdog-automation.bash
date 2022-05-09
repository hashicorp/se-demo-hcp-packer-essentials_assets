#!/bin/bash -l

# Check out source to a new branch folder
export BRANCH=$TF_DIR"-branch-"$(date +%s)

# Copy content to latest branch folder
mkdir -p $BRANCH

# Copy content to branch folder
cp $TF_DIR/production/*.tf $BRANCH

# Place TFC backend 

cat << EOF > $BRANCH/backend.tf
terraform {
    backend "remote" {
    organization = "$TFE_ORG"
    workspaces {
        name = "$TFE_WORKSPACE" 
        }
    }
}
EOF

cat << EOF > $BRANCH/.terraformrc
    credentials "app.terraform.io" {
    token = "$TFE_TOKEN"
}
EOF

export TF_CLI_CONFIG_FILE="${BRANCH}/.terraformrc"

# Initialize Terraform
terraform -chdir=$BRANCH init

# Declare Terraform Variables

export TFE_WORKSPACE_ID=$(curl -k -s \
  --header "Authorization: Bearer $TFE_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  $TFC_API_SHOW_WORKSPACE \
| jq -r '.data.id')

declare -a environment_vars=("HCP_CLIENT_ID" "HCP_CLIENT_SECRET" "AWS_ACCESS_KEY_ID" "AWS_SECRET_ACCESS_KEY")
for var in ${environment_vars[@]}; 
do 
    cat << EOF > create_var.json
{
    "data": {
      "type": "vars",
      "attributes": {
        "key": "$var",
        "value": "$(printenv $var)",
        "category": "env",
        "hcl": false,
        "sensitive": true
      },
      "relationships": {
        "workspace": {
          "data": {
            "id": "${TFE_WORKSPACE_ID}",
            "type": "workspaces"
          }
        }
      }
    }
  }
EOF
    
    RESPONSE=$(curl -k -s \
    --header "Authorization: Bearer $TFE_TOKEN" \
    --header "Content-Type: application/vnd.api+json" \
    --request POST \
    --data @create_var.json \
    $TFC_API_PUSH_VARS )
    
    rm -f create_var.json
done

# Get the HCP Packer runtask ID
# The integration must exist before this happens

RUNTASK_ID=$(curl -s -H "Authorization: Bearer $TFE_TOKEN" \
  $TFC_API_LIST_RUNTASK \
  | jq -r '.data | .[] | select( .attributes.name == "hcp-packer") | .id')

# Build the payload

cat << EOF > payload.json
{
  "data": {
    "type": "workspace-tasks",
      "attributes": {
        "enforcement-level": "mandatory"
      },
      "relationships": {
        "task": {
          "data": {
            "id": "${RUNTASK_ID}",
            "type": "tasks"
          }
        }
      }
  }
}
EOF

# Simplify the TFC API endpoint to attach the runtask to the workspace

export TFC_API_ATTACH_RUNTASK=${TCF_API_BASE_URL}/workspaces/${TFE_WORKSPACE_ID}/tasks

# Attach the runtask

RESPONSE=$(curl -s -k \
  -H "Authorization: Bearer $TFE_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  --request POST \
  --data @payload.json \
  $TFC_API_ATTACH_RUNTASK)

# Let's be tidy

rm -f payload.json

# Build Terraform
terraform -chdir=$BRANCH apply -auto-approve

# Remove TFC sensitive data from this branch
rm -f $BRANCH/.terraformrc