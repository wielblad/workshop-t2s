terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.60.0"
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

resource "azurerm_postgresql_flexible_server" "example" {
  name                   = "postgresql-server-postgres-user04"
  resource_group_name    = "rg-04"
  location               = "polandcentral"
  administrator_login    = "pgadmin"
  administrator_password = "admin"
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  version                = "13"
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_all" {
  name                = "AllowAllIPs"
  server_id           = azurerm_postgresql_flexible_server.example.id
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}

resource "azurerm_postgresql_flexible_server_database" "usersdb" {
  name      = "usersdb"
  server_id = azurerm_postgresql_flexible_server.example.id
  charset   = "UTF8"
  collation = "en_US.utf8"
  provisioner "local-exec" {
    command = "PGPASSWORD=admin psql -h ${azurerm_postgresql_flexible_server.example.fqdn} -U pgadmin -d usersdb -f ./init_usersdb.sql"
    environment = {
      PGPASSWORD = "admin"
    }
  }
  provisioner "local-exec" {
    command = "PGPASSWORD=admin psql -h ${azurerm_postgresql_flexible_server.example.fqdn} -U pgadmin -d usersdb -f ./init_blog.sql"
    environment = {
      PGPASSWORD = "admin"
    }
  }
}
