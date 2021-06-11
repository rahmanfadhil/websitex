# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateVPC.html

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.39.0"
    }
  }
}

# VARIABLES
# ------------------------------------------------------------------------------

variable "region" {
  description = "The AWS region to create resources in."
  default     = "ap-southeast-1"
}

variable "vpc_cdir" {
  description = "CIDR Block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.0.0/24"
}

variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.1.0/24"
}

variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.2.0/24"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]
}

variable "web_instance_type" {
  description = "EC2 instance type for running the web app"
  default     = "t2.micro"
}

variable "database_instance_type" {
  description = "RDS instance type for the PostgreSQL database"
  default     = "db.t3.micro"
}

variable "database_version" {
  description = "The PostgreSQL version number"
  default     = "13.1"
}

variable "database_allocated_storage" {
  description = "The allocated storage for database in gibibytes"
  default     = 10
  type        = number
}

variable "database_name" {
  description = "PostgreSQL database username"
  default     = "foo"
}

variable "database_username" {
  description = "PostgreSQL database username"
  default     = "bar"
}

variable "database_password" {
  description = "PostgreSQL database username"
  default     = "ASuperStrongPwd"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for user-uploaded files"
  default     = "websitex-media"
}

variable "project_name" {
  description = "The project name"
  default     = "websitex"
}

# PROVIDER
# ------------------------------------------------------------------------------

provider "aws" {
  region = var.region
}

# VPC (VIRTUAL PRIVATE CLOUD)
# ------------------------------------------------------------------------------

# Production VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cdir
  enable_dns_support   = true
  enable_dns_hostnames = true
}

# PUBLIC SUBNET
# ------------------------------------------------------------------------------

# Public subnet
resource "aws_subnet" "public_subnet_1" {
  cidr_block        = var.public_subnet_1_cidr
  vpc_id            = aws_vpc.main.id
  availability_zone = var.availability_zones[0]
  tags              = { Name = "Public Subnet 1" }
}

# Internet Gateway for the public subnet, so that we our web instance can
# access with the internet, like calling third-party APIs.
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Route table for the public subnet
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main.id

  # Route the public subnet traffic through the Internet Gateway
  route {
    gateway_id = aws_internet_gateway.main.id
    cidr_block = "0.0.0.0/0"
  }

  tags = { Name = "Public Route Table" }
}

# Associate the public subnet to the route table
resource "aws_route_table_association" "public_route_1_association" {
  route_table_id = aws_route_table.public_route_table.id
  subnet_id      = aws_subnet.public_subnet_1.id
}

# PRIVATE SUBNETS
# ------------------------------------------------------------------------------

# Private subnets. In order to create a DB subnet group, we must have at least
# 2 subnets in two different availibility zones.
resource "aws_subnet" "private_subnet_1" {
  cidr_block        = var.private_subnet_1_cidr
  vpc_id            = aws_vpc.main.id
  availability_zone = var.availability_zones[0]
  tags              = { Name = "Private Subnet 1" }
}
resource "aws_subnet" "private_subnet_2" {
  cidr_block        = var.private_subnet_2_cidr
  vpc_id            = aws_vpc.main.id
  availability_zone = var.availability_zones[1]
  tags              = { Name = "Private Subnet 2" }
}

# Route tables for the private subnets
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "Private Route Table" }
}

# Associate the private subnets to the route table
resource "aws_route_table_association" "private_route_1_association" {
  route_table_id = aws_route_table.private_route_table.id
  subnet_id      = aws_subnet.private_subnet_1.id
}
resource "aws_route_table_association" "private_route_2_association" {
  route_table_id = aws_route_table.private_route_table.id
  subnet_id      = aws_subnet.private_subnet_2.id
}

# SECURITY GROUP
# ------------------------------------------------------------------------------

# Security group for the public subnet (web server)
resource "aws_security_group" "web_security_group" {
  name        = "web_security_group"
  description = "Allow HTTP and HTTPS traffic from all sources."
  vpc_id      = aws_vpc.main.id

  # Allow SSH
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # TODO: restrict SSH access
  }

  # Allow incoming HTTP traffic
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow incoming HTTPS traffic
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Web Security Group"
  }
}

# Security group for the private subnets (database)
resource "aws_security_group" "db_security_group" {
  name        = "db_security_group"
  description = "Allow EC2 instances to access the database."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web_security_group.id]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "DB Security Group"
  }
}

# RDS
# ------------------------------------------------------------------------------

resource "aws_db_subnet_group" "main" {
  name        = "main_db_subnet_group"
  description = "The default DB subnet group"
  subnet_ids  = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_db_instance" "main" {
  name     = var.database_name
  username = var.database_username
  password = var.database_password

  engine            = "postgres"
  engine_version    = var.database_version
  instance_class    = var.database_instance_type
  allocated_storage = var.database_allocated_storage

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db_security_group.id]
  skip_final_snapshot    = true
}

# EC2
# ------------------------------------------------------------------------------

data "aws_ami" "ubuntu_focal" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}


resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu_focal.id
  instance_type               = var.web_instance_type
  subnet_id                   = aws_subnet.public_subnet_1.id
  key_name                    = aws_key_pair.deployer_key.key_name
  vpc_security_group_ids      = [aws_security_group.web_security_group.id]
  associate_public_ip_address = true

  tags = {
    Name = "Web Server"
  }
}

# S3
# ------------------------------------------------------------------------------

resource "aws_s3_bucket" "media" {
  acl    = "public-read"
  bucket = var.s3_bucket_name
}

resource "aws_iam_user" "app" {
  name = "${var.project_name}-app"
}

resource "aws_iam_access_key" "app" {
  user = aws_iam_user.app.name
}

resource "aws_iam_user_policy" "app_ro" {
  name = "allow_${aws_s3_bucket.media.id}_s3_bucket"
  user = aws_iam_user.app.name

  policy = jsonencode({
    "Version" = "2012-10-17",
    "Statement" = [{
      "Effect" = "Allow",
      "Action" = "s3:*",
      "Resource" = [
        "${aws_s3_bucket.media.arn}",
        "${aws_s3_bucket.media.arn}/*"
      ]
    }]
  })
}

# SSH KEY
# ------------------------------------------------------------------------------

resource "aws_key_pair" "deployer_key" {
  key_name   = "deployer-key-${var.region}"
  public_key = file("./deployer-key.pub")
}

# OUTPUTS
# ------------------------------------------------------------------------------

output "web_public_ip" {
  value = aws_instance.web.public_ip
}

output "web_public_dns" {
  value = aws_instance.web.public_dns
}

output "database_url" {
  value     = "psql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.name}"
  sensitive = true
}

output "aws_access_key_id" {
  value = aws_iam_access_key.app.id
}

output "aws_secret_access_key" {
  value     = aws_iam_access_key.app.secret
  sensitive = true
}

output "secrets" {
  sensitive = true
  value = templatefile("${path.module}/secrets.template.yml", {
    database   = aws_db_instance.main,
    access_key = aws_iam_access_key.app,
    s3_bucket  = aws_s3_bucket.media
  })
}

output "ansible_inventory" {
  value = "[web]\n${aws_instance.web.public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=./deployer-key"
}
