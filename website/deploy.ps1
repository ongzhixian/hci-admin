param([string]$envType="test") 

switch ($envType)
{
    "test" {
        Write-Host "Deploying to test environment (no-promote)"
        & gcloud app deploy --version=1 --quiet --no-promote
        break
    }

    "prod" {
        Write-Host "Deploying to production environment"
        & gcloud app deploy --version=1 --quiet
        break
    }

    "cron" {
        Write-Host "Deploying cron jobs to production"
        & gcloud app deploy cron.yaml --quiet
        break
    }

    "clean" {
        Write-Host "Clean and remove deployment artifacts bucket"
        & gsutil rm -r gs://asia.artifacts.hci-admin.appspot.com
        break
    }

    "logs" {
        & gcloud app logs tail -s default
        break
    }

    default {
        Write-Error "No setup found for $envType"
    }
}