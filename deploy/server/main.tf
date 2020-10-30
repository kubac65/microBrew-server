resource "docker_image" "server_image" {
  name = "kubac65/micro-brew-server:${var.image_version}"
}

resource "docker_container" "server_container" {
  name    = "${var.name_prefix}-server_container"
  image   = docker_image.server_image.latest
  restart = "always"
  ports {
    internal = 52100
    external = 52100
  }

  networks_advanced {
    name = var.backend_network_name
  }
  env = [
    "INFLUX_DB_HOST=${var.influx_db_host}",
    "INFLUX_DB_PORT=${var.influx_db_port}",
    "INFLUX_DB_USERNAME=${var.influx_db_username}",
    "INFLUX_DB_PASSWORD=${var.influx_db_password}",
    "COUCH_DB_HOST=${var.couch_db_host}",
    "COUCH_DB_PORT=${var.couch_db_port}",
    "COUCH_DB_USERNAME=${var.couch_db_username}",
    "COUCH_DB_PASSWORD=${var.couch_db_password}",
    "DB_NAME_PREFIX=${var.db_name_prefix}",
  ]
}
