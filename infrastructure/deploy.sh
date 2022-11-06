#!/bin/bash

# copy stack.yml to ec2 instance with scp
scp -i $HOME/.ssh/id_awskey stack.yml ec2-user@13.212.58.102:/home/ec2-user/stack.yml

# ssh to ec2 instance and run docker stack deploy
ssh -i $HOME/.ssh/id_awskey ec2-user@13.212.58.102 "docker stack deploy -c stack.yml websitex"


waypoint context create -server-addr=18.143.171.14:9701 -server-auth-token=BCkP8cw7qjrqo31TbDZKe1FNBvFBV6CjkghYbXUZ3XrMoVBp2f1LG7bo4CKnpCP8r4S1hQfdRw6RVdA3NvSaVUkiZnVjG6etVuMfwvz2zVadeJDGUWC24R1cSTqZQjDttTk3dSNdSZ5e2tvjJ
