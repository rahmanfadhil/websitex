# Resources:
# - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateVPC.html
# - https://github.com/finleap/tf-ecs-fargate-tmpl
# - https://medium.com/@martinzugnoni/terraform-a-django-app-into-ecs-fargate-in-as-few-steps-as-possible-92fefe0e1057
# - https://testdriven.io/blog/deploying-django-to-ecs-with-terraform/

# TODOS:
# - serve static files in S3 instead of whitenoise
# - move everything to the private subnets and setup NAT gateway to communicate with the internet.
# - setup SSL
# - setup Redis with ElastiCache
# - autoscale ecs tasks
# - seperate everything to individual modules
# - move from Docker HUB to ECR

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.39.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
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

variable "public_subnets_cidr" {
  description = "CIDR blocks for public subnets"
  default     = ["10.0.0.0/24", "10.0.1.0/24"]
}

variable "private_subnets_cidr" {
  description = "CIDR blocks for private subnets"
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]
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

variable "s3_bucket_name" {
  description = "S3 bucket name for user-uploaded files"
  default     = "websitex-media"
}

variable "project_name" {
  description = "The project name"
  default     = "websitex"
}

variable "docker_image_name" {
  description = "The project image repository"
  default     = "rahmanfadhil/websitex"
}

variable "app_version" {
  description = "The project image tag"
  default     = "1.2.10"
}

variable "health_check_path" {
  description = "The app health check endpoint"
  default     = "/ping/"
}

variable "container_port" {
  description = "The app port"
  default     = 8000
}

variable "environment" {
  description = "The app port"
  default     = "production"
}

variable "cache_node_type" {
  description = "The Redis cache node type"
  default     = "cache.t2.micro"
}

# PROVIDER
# ------------------------------------------------------------------------------

provider "aws" {
  region = var.region
}

# VPC (VIRTUAL PRIVATE CLOUD)
# ------------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cdir
}

# PUBLIC SUBNETS
# ------------------------------------------------------------------------------

# Public subnet
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  count             = length(var.public_subnets_cidr)
  cidr_block        = element(var.public_subnets_cidr, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = "${var.project_name}-${element(var.availability_zones, count.index)}-public-subnet"
  }
}

# Internet Gateway for the public subnet, so that we our web instance can
# access with the internet, like calling third-party APIs.
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Route table for the public subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # Route the public subnet traffic through the Internet Gateway
  route {
    gateway_id = aws_internet_gateway.main.id
    cidr_block = "0.0.0.0/0"
  }

  tags = { Name = "Public Route Table" }
}

# Associate the public subnet to the route table
resource "aws_route_table_association" "public" {
  route_table_id = aws_route_table.public.id
  count          = length(var.public_subnets_cidr)
  subnet_id      = element(aws_subnet.public.*.id, count.index)
}

# PRIVATE SUBNETS
# ------------------------------------------------------------------------------

# Private subnets. In order to create a DB subnet group, we must have at least
# 2 subnets in two different availibility zones.
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  count             = length(var.private_subnets_cidr)
  cidr_block        = element(var.private_subnets_cidr, count.index)
  availability_zone = element(var.availability_zones, count.index)
}

# Route tables for the private subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "Private Route Table" }
}

# Associate the private subnets to the route table
resource "aws_route_table_association" "private" {
  route_table_id = aws_route_table.private.id
  count          = length(var.private_subnets_cidr)
  subnet_id      = element(aws_subnet.private.*.id, count.index)
}

# SECURITY GROUP
# ------------------------------------------------------------------------------

resource "aws_security_group" "alb" {
  name   = "${var.project_name}-sg-alb-${var.environment}"
  vpc_id = aws_vpc.main.id

  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 443
    to_port          = 443
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name        = "${var.project_name}-sg-alb-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_security_group" "ecs_tasks" {
  name   = "${var.project_name}-sg-task-${var.environment}"
  vpc_id = aws_vpc.main.id

  ingress {
    protocol         = "tcp"
    from_port        = var.container_port
    to_port          = var.container_port
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    security_groups  = [aws_security_group.alb.id]
  }


  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name        = "${var.project_name}-sg-task-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_security_group" "database" {
  name        = "${var.project_name}-sg-db-${var.environment}"
  description = "Allow ECS tasks to access the database."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-sg-db-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_security_group" "cache" {
  name        = "${var.project_name}-sg-cache-${var.environment}"
  description = "Allow ECS tasks to access the cache database (Redis)."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Redis"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-sg-cache-${var.environment}"
    Environment = var.environment
  }
}

# # ECR
# # ------------------------------------------------------------------------------

# resource "aws_ecr_repository" "main" {
#   name                 = "${var.project_name}-${var.environment}"
#   image_tag_mutability = "MUTABLE"

#   image_scanning_configuration {
#     scan_on_push = false
#   }
# }

# resource "aws_ecr_lifecycle_policy" "main" {
#   repository = aws_ecr_repository.main.name

#   policy = jsonencode({
#     rules = [{
#       rulePriority = 1
#       description  = "keep last 10 images"
#       action = {
#         type = "expire"
#       }
#       selection = {
#         tagStatus   = "any"
#         countType   = "imageCountMoreThan"
#         countNumber = 10
#       }
#     }]
#   })
# }

# output "ecr_repository_url" {
#   value = aws_ecr_repository.main.repository_url
# }

# ECS
# ------------------------------------------------------------------------------

# Cluster
resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Service
resource "aws_ecs_service" "app_service" {
  name        = "${var.project_name}-web"
  cluster     = aws_ecs_cluster.app_cluster.arn
  launch_type = "FARGATE"

  enable_execute_command             = true
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
  health_check_grace_period_seconds  = 60
  desired_count                      = 1
  task_definition                    = aws_ecs_task_definition.web.arn

  network_configuration {
    assign_public_ip = true
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.public.*.id
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.app_alb_tg.arn
    container_name   = var.project_name
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
}
resource "aws_ecs_service" "celery" {
  name        = "${var.project_name}-celery"
  cluster     = aws_ecs_cluster.app_cluster.arn
  launch_type = "FARGATE"

  enable_execute_command             = true
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
  desired_count                      = 1
  task_definition                    = aws_ecs_task_definition.celery.arn

  network_configuration {
    assign_public_ip = true
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.public.*.id
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
}

# CloudWatch logs
resource "aws_cloudwatch_log_group" "web_task" {
  name = "/ecs/${var.project_name}/web-task"
}
resource "aws_cloudwatch_log_group" "celery_task" {
  name = "/ecs/${var.project_name}/celery-task"
}

# Task definition
resource "aws_ecs_task_definition" "web" {
  container_definitions = jsonencode([
    {
      "name" : "${var.project_name}",
      "image" : "${var.docker_image_name}:${var.app_version}",
      "cpu" : 256,
      "memory" : 512,
      "essential" : true,
      "environment" : [
        {
          "name" : "DATABASE_URL",
          "value" : "psql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.name}"
        },
        { "name" : "SENDGRID_API_KEY", "value" : "blahs" },
        { "name" : "ALLOWED_HOSTS", "value" : "${aws_alb.app_alb.dns_name}" },
        { "name" : "USE_HTTPS", "value" : "False" },
        { "name" : "AWS_STORAGE_BUCKET_NAME", "value" : "${aws_s3_bucket.main.bucket}" },
        { "name" : "REDIS_URL", "value" : "redis://redis:6379" },
        { "name" : "BROKER_URL", "value" : "sqs://" },
        { "name" : "AWS_SQS_QUEUE_URL", "value" : "${aws_sqs_queue.main.id}" }
      ],
      "linuxParameters" : {
        "initProcessEnabled" : true # enable ECS exec to run db migrations
      }
      "portMappings" : [
        {
          "containerPort" : "${var.container_port}",
          "hostPort" : "${var.container_port}",
          "protocol" : "tcp"
        }
      ],
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "${aws_cloudwatch_log_group.web_task.name}",
          "awslogs-region" : "${var.region}",
          "awslogs-stream-prefix" : "ecs"
        }
      },
    }
  ])
  family                   = "${var.project_name}-web"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  cpu          = "256"
  memory       = "512"
  network_mode = "awsvpc"

  tags = {
    Environment = var.environment
  }
}

resource "aws_ecs_task_definition" "celery" {
  container_definitions = jsonencode([
    {
      "name" : "${var.project_name}",
      "image" : "${var.docker_image_name}:${var.app_version}",
      "cpu" : 256,
      "memory" : 512,
      "essential" : true,
      "command" : ["celery", "-A", "config", "worker", "-l", "info"]
      "environment" : [
        {
          "name" : "DATABASE_URL",
          "value" : "psql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.name}"
        },
        { "name" : "SENDGRID_API_KEY", "value" : "blahs" },
        { "name" : "ALLOWED_HOSTS", "value" : "${aws_alb.app_alb.dns_name}" },
        { "name" : "USE_HTTPS", "value" : "False" },
        { "name" : "AWS_STORAGE_BUCKET_NAME", "value" : "${aws_s3_bucket.main.bucket}" },
        { "name" : "REDIS_URL", "value" : "redis://redis:6379" },
        { "name" : "BROKER_URL", "value" : "sqs://" },
        { "name" : "AWS_SQS_QUEUE_URL", "value" : "${aws_sqs_queue.main.id}" }
      ],
      "portMappings" : [
        {
          "containerPort" : "${var.container_port}",
          "hostPort" : "${var.container_port}",
          "protocol" : "tcp"
        }
      ],
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "${aws_cloudwatch_log_group.celery_task.name}",
          "awslogs-region" : "${var.region}",
          "awslogs-stream-prefix" : "ecs"
        }
      },
    }
  ])
  family                   = "${var.project_name}-celery"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  cpu          = "256"
  memory       = "512"
  network_mode = "awsvpc"

  tags = {
    Environment = var.environment
  }
}

# LOAD BALANCER
# ------------------------------------------------------------------------------

resource "aws_alb" "app_alb" {
  name            = "${var.project_name}-alb"
  subnets         = aws_subnet.public.*.id
  security_groups = [aws_security_group.alb.id]
  internal        = false
}

resource "random_string" "alb_prefix" {
  length  = 4
  upper   = false
  special = false
}

resource "aws_alb_target_group" "app_alb_tg" {
  name        = "${var.project_name}-alb-tg-${random_string.alb_prefix.result}"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = var.health_check_path
    unhealthy_threshold = "2"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_alb_listener" "app_alb_listener" {
  load_balancer_arn = aws_alb.app_alb.id
  port              = 80
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.app_alb_tg.id
    type             = "forward"
  }
}

output "app_dns_lb" {
  description = "DNS load balancer"
  value       = aws_alb.app_alb.dns_name
}

# IAM
# ------------------------------------------------------------------------------

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        "Effect" : "Allow",
        "Sid" : ""
      }
    ]
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecsTaskRole"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        "Effect" : "Allow",
        "Sid" : ""
      },
    ]
  })
}

resource "aws_iam_policy" "ecs_task_policy" {
  name = "${var.project_name}_ecs_task_policy"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ],
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : "s3:*",
        "Resource" : [
          "${aws_s3_bucket.main.arn}",
          "${aws_s3_bucket.main.arn}/*"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : "sqs:*",
        "Resource" : ["${aws_sqs_queue.main.arn}"]
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-policy-attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}

# S3
# ------------------------------------------------------------------------------

resource "aws_s3_bucket" "main" {
  bucket = var.s3_bucket_name
  acl    = "public-read"
}

# RDS
# ------------------------------------------------------------------------------

resource "aws_db_subnet_group" "main" {
  subnet_ids = aws_subnet.private.*.id
}

resource "random_password" "database_password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

resource "aws_db_instance" "main" {
  engine                 = "postgres"
  engine_version         = var.database_version
  instance_class         = var.database_instance_type
  allocated_storage      = var.database_allocated_storage
  name                   = var.database_name
  username               = var.database_username
  password               = random_password.database_password.result
  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  skip_final_snapshot    = true
}

# SQS
# ------------------------------------------------------------------------------

resource "aws_sqs_queue" "main" {
  name                      = "${var.project_name}-queue"
  max_message_size          = 2048
  message_retention_seconds = 86400

  tags = {
    Environment = var.environment
  }
}
