# Matchvote Operations
A collection of scripts and artifacts used for various infrastructure and development operations.  

### Dependencies
* Docker

### Setup
    bin/build

### Kubernetes Deployment
- Update relevent k8s config file `image` to target version
- `bin/deploy <app>` (this deploys migrant first)

### Accessing RDS instance
- `ssh -i /path/to/.pem <bastion url>`
- `psql <db> -U <user> -h <rds host>`

### Utilities - Deprecated
* Create a new Cloudformation stack from a template: `bin/create_stack <stack-name>`
* Delete a stack: `bin/delete_stack <stack-name>`
* Check the status of a stack: `bin/stack_status <stack-name>`

### K8S Secrets
The values in a secrets.yml value must be base64 encoded. To do this at the command line:

    echo -n "value" | base64