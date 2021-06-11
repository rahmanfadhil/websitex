#!/usr/bin/env bash

set -e

ANSIBLE_VAULT_PASSWORD_FILE="$PWD/vault_password"
ANSIBLE_INVENTORY_FILE="$PWD/hosts"
SECRETS_FILE="$PWD/secrets.yml"
SSH_KEY="$PWD/deployer-key"

# if [ ! -f "$ANSIBLE_VAULT_PASSWORD_FILE" ]; then
#     echo "🔑 Ansible vault password file does not exists!"
#     echo "Write your ansible vault password in $ANSIBLE_VAULT_PASSWORD_FILE to send sensitive information to the virtual machine."
#     exit 1
# fi

# if [ ! -f "$SSH_KEY" ]; then
#     echo "SSH keypair not found!"
#     echo "🔑 Creating a new SSH keypair in $SSH_KEY..."
#     ssh-keygen -t rsa -N "" -b 2048 -C "deployer" -f $SSH_KEY
#     sudo chmod 600 $SSH_KEY
#     echo "SSH keypair successfully created!"
#     echo "  Secret key => $SSH_KEY"
#     echo "  Public key => $SSH_KEY.pub"
# fi

# echo "🛠 Initializing Terrraform project..."
# terraform init
# echo "Terraform project successfully created!"

echo "🏗 Applying AWS infrastructure with Terraform..."
terraform apply -auto-approve
echo "Your AWS infrasture has been successfully created!"

echo "📝 Creating Ansible inventory from Terraform output..."
terraform output -raw ansible_inventory > $ANSIBLE_INVENTORY_FILE
echo "Your Ansible inventory is available in $ANSIBLE_INVENTORY_FILE"

echo "🔑 Encrypting RDS credentials with Ansible Vault..."
terraform output -raw secrets > $SECRETS_FILE
ansible-vault encrypt --vault-password-file $ANSIBLE_VAULT_PASSWORD_FILE $SECRETS_FILE
echo "Your encrypted RDS credentials are available in $SECRETS_FILE"

echo "⚙️ Running Ansible playbook..."
ansible-playbook -i $ANSIBLE_INVENTORY_FILE -e "@$SECRETS_FILE" --vault-password-file $ANSIBLE_VAULT_PASSWORD_FILE provision.yml
echo "🚀 Successfully deployed your app!"
