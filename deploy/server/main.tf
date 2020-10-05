resource "docker_image" "server_image" {
    name = "kubac65/micro-brew-server:${var.image_version}"
}

resource "docker_container" "server_container" {
    name = "${var.name_prefix}-server_container"
    image = docker_image.server_image.latest
    restart = "always"
    ports {
        internal = 52100
        external = 52100
    }

    networks_advanced {
        name = var.backend_network_name
    }
    env = [
        "TS_DB_HOST=${var.timeseriesdb_host}",
        "TS_DB_PORT=${var.timeseriesdb_port}",
        "TS_DB_USERNAME=${var.timeseriesdb_username}",
        "TS_DB_PASSWORD=${var.timeseriesdb_password}",
        "TS_DB_DATABASE=${var.timeseriesdb_dbname}",
        "BR_DB_HOST=${var.brewdb_host}",
        "BR_DB_PORT=${var.brewdb_port}",
        "BR_DB_USERNAME=${var.brewdb_username}",
        "BR_DB_PASSWORD=${var.brewdb_password}",
        "BR_DB_DATABASE=${var.brewdb_dbname}"
    ]
}