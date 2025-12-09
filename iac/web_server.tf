resource "azurerm_container_registry" "acr" {
  name = "acr${random_integer.ri_number.result}"
  resource_group_name = data.azurerm_resource_group.arg.name
  location = data.azurerm_resource_group.arg.location
  sku = "Basic"
  admin_enabled = true
}


resource "azurerm_service_plan" "asp" {
  name                = "aspchatbot"
  resource_group_name = data.azurerm_resource_group.arg.name
  location            = data.azurerm_resource_group.arg.location
  os_type             = "Linux"
  sku_name            = "S1"
}


resource "azurerm_linux_web_app" "app" {
  name                = "appchatbot${random_integer.ri_number.result}"
  resource_group_name = data.azurerm_resource_group.arg.name
  location            = data.azurerm_resource_group.arg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      docker_image_name = "${azurerm_container_registry.acr.login_server}/dashboard:latest"
      docker_registry_url = "http://${azurerm_container_registry.acr.login_server}"
    }
  }
}




