variable "backend_network_name" {}
variable "name_prefix" {}
variable "image_version" {
  default = "latest"
}

variable "influxdb_user" {}
variable "influxdb_password" {}
variable "influxdb_dbname" {}
