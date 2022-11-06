provider "aws" {
  region = local.region
}

data "aws_caller_identity" "current" {}

locals {
  name             = "websitex"
  region           = "ap-southeast-1"
  current_identity = data.aws_caller_identity.current.arn
  environment      = "dev"

  tags = {
    Project     = local.name
    Owner       = "user"
    Terraform   = "true"
    Environment = local.environment
  }
}

################################################################################
# Supporting Resources
################################################################################

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = local.name
  cidr = "10.99.0.0/18"

  azs              = ["${local.region}a", "${local.region}b", "${local.region}c"]
  public_subnets   = ["10.99.0.0/24", "10.99.1.0/24", "10.99.2.0/24"]
  private_subnets  = ["10.99.3.0/24", "10.99.4.0/24", "10.99.5.0/24"]
  database_subnets = ["10.99.7.0/24", "10.99.8.0/24", "10.99.9.0/24"]

  create_database_subnet_group       = true
  create_database_subnet_route_table = true

  tags = local.tags
}

module "database_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "${local.name}-database-sg"
  description = "Security group for PostgreSQL database on RDS"
  vpc_id      = module.vpc.vpc_id

  computed_ingress_with_source_security_group_id = [{
    rule                     = "postgresql-tcp"
    source_security_group_id = module.instance_security_group.security_group_id
  }]
  number_of_computed_ingress_with_source_security_group_id = 1

  egress_rules = ["all-all"]

  tags = local.tags
}

module "instance_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "${local.name}-instance-sg"
  description = "Security group for example usage with EC2 instance"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp", "ssh-tcp"]
  egress_rules        = ["all-all"]

  # allow the world to access port 9701 (Waypoint) on the instance
  ingress_with_cidr_blocks = [{
    protocol    = "tcp"
    from_port   = 9701
    to_port     = 9701
    description = "Waypoint"
    cidr_blocks = "0.0.0.0/0"
  }]

  tags = local.tags
}


################################################################################
# RDS Module
################################################################################

# module "db" {
#   source  = "terraform-aws-modules/rds/aws"
#   version = "~> 5.0"

#   identifier = local.name

#   # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
#   engine               = "postgres"
#   engine_version       = "14.2"
#   family               = "postgres14" # DB parameter group
#   major_engine_version = "14"         # DB option group
#   instance_class       = "db.t3.micro"

#   allocated_storage     = 5
#   max_allocated_storage = 100

#   # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
#   # "Error creating DB Instance: InvalidParameterValue: MasterUsername
#   # user cannot be used as it is a reserved word used by the engine"
#   db_name  = "${local.name}_db"
#   username = "${local.name}_user"
#   port     = 5432

#   multi_az               = true
#   db_subnet_group_name   = module.vpc.database_subnet_group
#   vpc_security_group_ids = [module.database_security_group.security_group_id]

#   maintenance_window              = "Mon:00:00-Mon:03:00"
#   backup_window                   = "03:00-06:00"
#   enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
#   create_cloudwatch_log_group     = true

#   backup_retention_period = 1
#   skip_final_snapshot     = true
#   deletion_protection     = false

#   performance_insights_enabled          = true
#   performance_insights_retention_period = 7
#   create_monitoring_role                = true
#   monitoring_interval                   = 60
#   monitoring_role_name                  = "example-monitoring-role-name"
#   monitoring_role_use_name_prefix       = true
#   monitoring_role_description           = "Description for monitoring role"

#   parameters = [
#     {
#       name  = "autovacuum"
#       value = 1
#     },
#     {
#       name  = "client_encoding"
#       value = "utf8"
#     }
#   ]

#   tags = local.tags
#   db_option_group_tags = {
#     "Sensitive" = "low"
#   }
#   db_parameter_group_tags = {
#     "Sensitive" = "low"
#   }
# }

################################################################################
# EC2 Instance
################################################################################

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

data "local_file" "ssh_public_key" {
  filename = pathexpand("~/.ssh/id_awskey.pub")
}

resource "aws_key_pair" "ssh_key" {
  public_key = data.local_file.ssh_public_key.content
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  vpc_security_group_ids = [module.instance_security_group.security_group_id]
  subnet_id              = module.vpc.public_subnets[0]
  key_name               = aws_key_pair.ssh_key.key_name
  monitoring             = true

  tags = local.tags

  user_data                   = <<-EOF
    #!/bin/bash
    sudo apt-get update -y
    sudo apt-get remove -y docker docker-engine docker.io containerd runc
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo usermod -aG docker ubuntu
    sudo systemctl enable docker
    sudo systemctl start docker

    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update -y && sudo apt-get install -y waypoint
    waypoint install -platform=docker -accept-tos
  EOF
  user_data_replace_on_change = true
}

resource "aws_ecr_repository" "app" {
  name                 = "${local.name}-${local.environment}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ip_address" {
  value = aws_instance.web.public_ip
}

output "ecr_url" {
  value = aws_ecr_repository.app.repository_url
}

# output "db_instance_url" {
#   sensitive = true
#   value     = "postgresql://${module.db.db_instance_username}:${module.db.db_instance_password}@${module.db.db_instance_endpoint}/${module.db.db_instance_name}"
# }

# resource "local_file" "ansible_inventory" {
#   content = templatefile("${path.module}/ansible/inventory.tpl", {
#     ip_address = aws_instance.web.public_ip
#   })
#   filename = "${path.module}/ansible/inventory.ini"
# }
