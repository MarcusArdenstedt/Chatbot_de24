resource "azurerm_service_plan" "asp" {
  name                = ""
  resource_group_name = ""
  location            = ""
  os_type             = "Linux"
  sku_name            = "S1"
}


resource "azurerm_linux_web_app" "app" {
  name                = ""
  resource_group_name = ""
  location            = ""
  service_plan_id     = ""

}


