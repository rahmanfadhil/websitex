project = "websitex"

app "websitex" {
    labels = {
        service = "websitex"
        env = "dev"
    }

    build {
        use "docker" {}
    }

    deploy {
        use "docker" {
            command      = ["ps"]
            service_port = 8000
            static_environment = {
                "PORT": "8000"
                "DATABASE_URL": "postgres://postgres:postgres@postgres:5432/postgres"
                "REDIS_URL": "redis://redis:6379"
                "EMAIL_HOST": "mailhog"
                "EMAIL_PORT": "1025"
                "AWS_STORAGE_BUCKET_NAME":"websitex"
            }
        }
    }
}
