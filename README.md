# HCP Packer Essentials - Assets

Create, manage and release machine images across multiple platforms.

## Resources

| Resource | Description |
|----------|:------------|
| Platform | [Instruqt][1] |
| Demo Script| HCP Packer Essentials - [Demo Guide][2] |
| Slides | HCP Packer Essentials - [Presentation][3] |
| Recording | HCP Packer Essentials - [Recording][4] |
| GitHub Assets | HCP Packer Essentials - [Instruqt Track][5] |
| Contributors | Joe Thompson, Gilberto Castillo |

## Innovation Lab: How to engage

- New content requests: [Field Request form][6] (use the Asset request type)
- On Slack: [#proj-instruqt][7] for Instruqt questions and issues

  - For access to HashiCorp Instruqt content, create an Instruqt account with your HashiCorp e-mail, then use the `/instruqt_access` integration in **#proj-instruqt** (see pinned messages for instructions)

  - Issues with upcoming/in-progress workshops/demos: tag **@team-innovation-lab** in **#proj-instruqt** (note that outside of US hours response may not be immediate at this time)

---
# `this`

This repo contains a number of assets that for the demonstration. 

## `.assets.api`

The API folder provides a simple utility with URL shortcuts for API-driven operations for ease of reading, updating and controlling. The URL shortcuts are applicable to HCP Packer and Terraform Cloud. 

For instance, the required ULR to create a channel in the HCP registry is as follows:

```bash
https://api.cloud.hashicorp.com/packer/2021-04-30/organizations/ac1ee2f1-42a7-4165-4efd-379187552e02/projects/4f204934-68cb-4165-43e7-abc91fb8987d
```

With the operation is implemented as follows:

```bash
curl -s -H "Authorization: Bearer *********" \
  -H "Content-Type: application/json" \
  -d '{"slug" : "hashicups-development", "incremental_version": 1}' \
  -X POST https://api.cloud.hashicorp.com/packer/2021-04-30/organizations/ac1ee2f1-42a7-4165-4efd-379187552e02/projects/4f204934-68cb-4165-43e7-abc91fb8987d/images/hashicups-frontend-ubuntu/channels
```

For ease of readability, update and future control, we can express the requirements with Bash shortcuts as follows:

```bash
# Our given identity during the set up stage
export HCP_ORGANIZATION_ID=ac1ee2f1-42a7-4165-4efd-379187552e02
export HCP_PROJECT_ID=4f204934-68cb-4165-43e7-abc91fb8987d

# This is generated dynamically
export HCP_CLIENT_TOKEN="*********"

# Specific to this exercise
export HCP_PACKER_BUCKET_SLUG="hashicups-frontend-ubuntu"
export HCP_PACKER_CHANNEL_SLUG="hashicups-development"

# Generic API endpoint for HCP Packer
export HCP_PACKER_BASE_URL=https://api.cloud.hashicorp.com/packer/2021-04-30/organizations/${HCP_ORGANIZATION_ID}/projects/${HCP_PROJECT_ID}

# URL Shortcut
export HCP_PACKER_API_CREATE_CHANNEL=${HCP_PACKER_BASE_URL}/images/${HCP_PACKER_BUCKET_SLUG}/channels
```

With the URL shortcuts, the operation implemented in the track is easier to interpret and explain during a demonstration:

```bash
curl -s -H "Authorization: Bearer ${HCP_CLIENT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"slug" : "'"${HCP_PACKER_CHANNEL_SLUG}"'", "incremental_version": 1}' \
  -X POST $HCP_PACKER_API_CREATE_CHANNEL
```

## `.assets.packer`

The [Packer](./assets/packer/) folder contains the Packer templates that users modify during the demonstration.

Notable is the use of [setup-deps-hashicups.sh](./assets/packer/production/setup-deps-hashicups.sh) to deploy the HashiCups application. The setup-deps-hashicups.sh is copied from [`learn-packer-multicloud`][8] courtesy of our Learn Team.

## `.assets.terraform`

The [Terraform](./assets/terraform/) folder contains deployment templates for Terraform. While the content is distributed across development and production, the same material is used in both exercises. However, during the first technical challenge during the demonstration, the user creates a local deployment under the development folder - which subsequently contains a Terraform state file.

## `.assets.watchdog`

The [watchdog](./assets/watchdog/) folder contains a custom Python program to monitor arbitrary changes in a given directory. When changes are detected, the Python program launches a back-end script to do the following:

1. Copy the Terraform production folder - simulating a branch fork
2. Crate a backend template for a workspace in Terraform Cloud
3. Create a template for `terraformrc` 
4. Initialize Terraform - which creates the TFC workspace
5. Upload required AWS and HCP credentials to the TFC workspace
6. Get the HCP Packer runtask ID from the TFC org (if it exists)
7. Attach the HCP Packer runtask to the TFC workspace
8. Run remote `terraform apply` for the TFC workspace
9. Tidy up and remove TFC sensitive data from this branch 

## `.www`

The [`www`](./www) folder contains our custom `Explainer` Flask application. The application is intantiated in the demonstration as a production item. It's purpose is to provide an interactive visual guide during the demonstration. 

The motivation for this Explainer is to make use of the real estate available in the Instruqt Track during the demonstration. The material is identical to the slides in the HCP Packer Essentials - [Presentation][3].

[1]: <https://play.instruqt.com/hashicorp/tracks/hcp-packer-essentials> "HCP Packer Essentials - Instruqt Track"
[2]: <https://docs.google.com/document/d/1a8JTFHj6WiEcHNVLKaiA7218FrJuraUy8b9Kub1nxrM/edit?usp=sharing> "HCP Packer Essentials - Demo Guide"
[3]: <https://docs.google.com/presentation/d/1DPT6DLvk6MVa46pTObDnjKxNqeXZBeVfXkgacW-UmWc/edit?usp=sharing> "HCP Packer Essentials - Presentation"
[4]: <https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley> "HCP Packer Essentials - Recording"
[5]: <https://github.com/hashicorp/se-demo-hcp-packer-essentials> "HCP Packer Essentials - Instruqt Track"
[6]: <https://hashicorp.wufoo.com/forms/field-requests-products-assets> "Field Request form"
[7]: <https://hashicorp.slack.com/archives/CGYB4R3NX> "proj-instruct"
[8]: <https://github.com/hashicorp/learn-packer-multicloud> "setup-deps-hashicups.sh"