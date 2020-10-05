variable "backend_network_name" {}
variable "name_prefix" {}
variable "image_version" {
    default = "latest"
}

variable "timeseriesdb_host" {}
variable "timeseriesdb_port" {}
variable "timeseriesdb_username" {}
variable "timeseriesdb_password" {}
variable "timeseriesdb_dbname" {}

variable "brewdb_host" {}
variable "brewdb_port" {}
variable "brewdb_username" {}
variable "brewdb_password" {}
variable "brewdb_dbname" {}