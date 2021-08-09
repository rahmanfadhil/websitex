#!/bin/sh

set -e

if [ ! -d ".terraform" ]
then
    terraform init
fi

terraform apply -auto-approve

CLUSTER=$(terraform output -raw ecs_cluster_name)
TASK_DEFINITION=$(terraform output -raw latest_task_definition)
SUBNETS=$(terraform output -json public_subnets)
SECURITY_GROUPS=$(terraform output -json security_groups)

aws ecs run-task --task-definition $TASK_DEFINITION \
    --cluster $CLUSTER \
    --count 1 \
    --launch-type FARGATE \
    --overrides "{\"containerOverrides\": [{\"name\": \"app\", \"command\": [\"python\", \"manage.py\", \"migrate\"]}]}" \
    --network-configuration "{\"awsvpcConfiguration\": {\"subnets\": $SUBNETS, \"securityGroups\": $SECURITY_GROUPS, \"assignPublicIp\": \"ENABLED\"}}" \
    --no-cli-pager
