#!/bin/sh

# Execute a command in AWS ECS

CLUSTER=$(terraform output -raw ecs_cluster_name)

TASKS=$(aws ecs list-tasks --cluster $CLUSTER --service-name web --max-items 1)
TASK_ARN=$(echo $TASKS | grep -o '"arn:[^"]\+"' | tr -d '"')

aws ecs execute-command --cluster $CLUSTER \
    --task $TASK_ARN \
    --container app \
    --interactive \
    --command "/bin/sh"
