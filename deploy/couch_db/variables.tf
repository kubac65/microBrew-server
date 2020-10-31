variable "backend_network_name" {}
variable "name_prefix" {}
variable "image_version" {
  default = "3.1.1-debian-10-r39"
}

variable "couchdb_user" {}
variable "couchdb_password" {}
