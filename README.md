# t2sworkshop

Participants learned how to set up a fully automated, secure CI/CD pipeline for deploying a Flask web application to Azure using **GitHub Actions** and **passwordless authentication via Federated Identity**.

## Key Topics Covered
- Creating and configuring a GitHub repository
- Setting up Azure resources:
  - User Assigned Managed Identity
  - Azure Blob Storage for Terraform state
  - Azure Container Registry (ACR)
  - App Service and Service Plan (from terraform)
- Configuring GitHub Secrets for secure integration
- Writing and deploying:
  - `Dockerfile`
  - `app.py` (Flask application)
  - `main.tf` (Terraform configuration)
  - GitHub Actions workflow (`deploy.yml`)
- **Passwordless authentication using OIDC federation** between GitHub and Azure
- Secure infrastructure and app deployment using Infrastructure as Code (IaC)

This workshop showcased best practices for modern DevOps workflows with **Terraform**, **containerization**, and **secure CI/CD pipelines** on Azure.

# Instruction
## 1. Create Free GitHub Account
    - Write down your user name
    - Create empty repo with README.md file
    - write down repo name

## 2. Log into Azure Account
    - Find your Resource Group


test