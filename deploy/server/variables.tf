variable "backend_network_name" {}
variable "name_prefix" {}
variable "image_version" {
  default = "latest"
}

variable "influx_db_host" {}
variable "influx_db_port" {}
variable "influx_db_username" {}
variable "influx_db_password" {}

variable "couch_db_host" {}
variable "couch_db_port" {}
variable "couch_db_username" {}
variable "couch_db_password" {}

variable "db_name_prefix" {}
