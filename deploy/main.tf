terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
    }
  }
}

provider "docker" {}

resource "docker_network" "backend_network" {
  name = "${var.name_prefix}-backend_network"
}

module "influx_db" {
  source               = "./influx_db"
  name_prefix          = var.name_prefix
  backend_network_name = docker_network.backend_network.name
  influxdb_user        = var.timeseriesdb_username
  influxdb_password    = var.timeseriesdb_password
  influxdb_dbname      = var.timeseriesdb_dbname
}

module "couch_db" {
  source               = "./couch_db"
  name_prefix          = var.name_prefix
  backend_network_name = docker_network.backend_network.name
  couchdb_user         = var.brewdb_username
  couchdb_password     = var.brewdb_password
}

module "server" {
  source               = "./server"
  name_prefix          = var.name_prefix
  backend_network_name = docker_network.backend_network.name

  timeseriesdb_host     = module.influx_db.host
  timeseriesdb_port     = module.influx_db.port
  timeseriesdb_username = var.timeseriesdb_username
  timeseriesdb_password = var.timeseriesdb_password
  timeseriesdb_dbname   = var.timeseriesdb_dbname

  brewdb_host     = module.couch_db.host
  brewdb_port     = module.couch_db.port
  brewdb_username = var.brewdb_username
  brewdb_password = var.brewdb_password
  brewdb_dbname   = var.brewdb_dbname
}
