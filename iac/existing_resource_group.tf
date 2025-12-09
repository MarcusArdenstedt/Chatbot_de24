data "azurerm_resource_group" "arg" {
    name = "rgchatbotde24"
}

output "id" {
    value = data.azurerm_resource_group.arg.id
}