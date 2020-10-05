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

module "timeseries_db" {
  source               = "./timeseries_db"
  name_prefix          = var.name_prefix
  backend_network_name = docker_network.backend_network.name
  influxdb_user = var.timeseriesdb_username
  influxdb_password = var.timeseriesdb_password
  influxdb_dbname = var.timeseriesdb_dbname
}

module "brew_db" {
  source = "./brew_db"
  name_prefix = var.name_prefix
  backend_network_name = docker_network.backend_network.name
  couchdb_user = var.brewdb_username
  couchdb_password = var.brewdb_password
}

module "server" {
  source = "./server"
  name_prefix = var.name_prefix
  backend_network_name = docker_network.backend_network.name

  timeseriesdb_host = module.timeseries_db.host
  timeseriesdb_port = module.timeseries_db.port
  timeseriesdb_username = var.timeseriesdb_username
  timeseriesdb_password = var.timeseriesdb_password
  timeseriesdb_dbname = var.timeseriesdb_dbname

  brewdb_host = module.brew_db.host
  brewdb_port = module.brew_db.port
  brewdb_username = var.brewdb_username
  brewdb_password = var.brewdb_password
  brewdb_dbname = var.brewdb_dbname
}