terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}
provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-04"
    storage_account_name = "storageworkshop04"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_service_plan" "example" {
  name                = "example-app-service-plan-user04"
  location            = "westeurope"
  resource_group_name = "rg-04"
  os_type             = "Linux"
  sku_name            = "P0v3"
}


resource "azurerm_linux_web_app" "example" {
  name                = "example-webapp-user04"
  location            = "westeurope"
  resource_group_name = "rg-04"
  service_plan_id     = azurerm_service_plan.example.id
  site_config {}
}

resource "azurerm_storage_account" "example" {
  name                     = "storageaccountuser04"
  resource_group_name      = "rg-04"
  location                 = "westeurope"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}

resource "azurerm_container_group" "rabbitmq" {
  name                = "rabbitmq-group"
  location            = "westeurope"
  resource_group_name = "rg-04"
  os_type             = "Linux"

  container {
    name   = "rabbitmq"
    image  = "rabbitmq:3-management"
    cpu    = "1.0"
    memory = "1.5"

    ports {
      port     = 5672
      protocol = "TCP"
    }
    ports {
      port     = 15672
      protocol = "TCP"
    }
    environment_variables = {
      RABBITMQ_DEFAULT_USER = "admin"
      RABBITMQ_DEFAULT_PASS = "adminpassword"
    }
  }

  ip_address_type = "Public"
  dns_name_label  = "rabbitmquser04"
}
