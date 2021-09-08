# WebsiteX

A production-ready Django boilerplate based on [DjangoX](https://github.com/wsvincent/djangox).

## Features

-   Django 3.2
-   PostgreSQL 13
-   Memcached for caching
-   RabbitMQ for Celery tasks
-   A blog with [Wagtail CMS](https://wagtail.io/)
-   Bootstrap 5 with Webpack 5
-   Static files compression with Brotli (HTTPS) or Gzip (HTTP)

**Development**

-   Ready to go docker compose stack
-   [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) to debug the app
-   [pytest](https://django-debug-toolbar.readthedocs.io/en/latest/) for unit testing
-   [ipython](https://django-debug-toolbar.readthedocs.io/en/latest/) for interactive python/django shell

**Other Dependencies**

-   [django-anymail](https://django-environ.readthedocs.io/en/latest/) to for sending emails in production.
-   [whitenoise](http://whitenoise.evans.io/en/stable/index.html) to serve static files in production.
-   [gunicorn](https://gunicorn.org/) to run server in production environment.

## Development

Everything is bundled up in a single Docker Compose configuration. So, once you have [Docker](https://www.docker.com/) installed on your machine, run this command.

```
$ docker-compose up -d
```

## Deployment

This boilerplate comes with a [Terraform](https://www.terraform.io/) code that allows you to deploy the entire application stack to [Amazon Web Service](https://aws.amazon.com).

-   Deploy containerized app to [Amazon ECS](https://aws.amazon.com/ecs/) cluster with rollback if health checks failed
-   Run commands on production container via [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html)
-   Upload files to an [AWS S3](https://aws.amazon.com/s3/) bucket
-   Send transactional emails via [Amazon SES](https://aws.amazon.com/ses/)
-   Managed PostgreSQL database on [RDS](https://aws.amazon.com/rds/)
-   Managed Memcached cluster on [ElasiCache](https://aws.amazon.com/elasticache/)
-   Managed RabbitMQ server on [Amazon MQ](https://aws.amazon.com/amazon-mq/)
-   Use custom domain/subdomain with [Route53](https://aws.amazon.com/route53/) (optional)
-   Managed HTTPS certificate with [AWS Certificate Manager](https://aws.amazon.com/acm/) (optional)
-   HTTP/2 with [Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/) (only if HTTPS is enabled)

### Prerequisites

-   An AWS account.
-   An email address for sending transactional emails via SES.
-   [AWS CLI](https://aws.amazon.com/cli/) installed on your machine.
-   [Terraform](https://www.terraform.io/intro/getting-started/install.html) installed on your machine.
-   [Docker](https://docs.docker.com/get-docker/) installed on your machine.

### Provisioning

1.  [Configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) AWS CLI.

    Grab your access key id and secret from the your AWS dashboard and run the `aws configure` command in your terminal.

    ![How to get the access key from your AWS dashboard](./docs/aws-secret-key.jpg)

    ```
    $ aws configure
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: json
    ```

2.  Copy Terraform [variable definitions](https://www.terraform.io/docs/language/values/variables.html#variable-definitions-tfvars-files) from the template file and update the values accordingly.

    ```
    $ cp terraform.tfvars.template terraform.tfvars
    $ cat terraform.tfvars
    region             = "ap-southeast-1"
    availability_zones = ["ap-southeast-1a", "ap-southeast-1b"]
    docker_image_name  = "rahmanfadhil/websitex:1.7"
    project_name       = "websitex"
    environment        = "production"

    # TODO: Change this to your own values
    ses_email_address = null
    domain_name       = null
    certificate_arn   = null
    ```

3.  Run the deploy script.

    ```
    $ ./deploy.sh
    ```

4.  Verify SES email.

    ![Verify SES email](./docs/ses-verification-email.jpg)

## Using a custom domain

If you use a custom domain, make sure to update the name servers of your domain. You can see the settings from the terraform ouput by running the command below.

```
$ terraform output -json name_servers
```

## Using a custom domain

In progress...

### Deploying new version

1. Update the docker image url in `terraform.tfvars` file.

    ```
    # other config...
    docker_image_name  = "rahmanfadhil/websitex:1.7" # edit this line
    ```

2. Run the deploy script.

    ```
    $ ./deploy.sh
    ```
