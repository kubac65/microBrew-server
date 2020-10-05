resource "docker_volume" "influxdb_volume" {
    name = "${var.name_prefix}-influxdb_volume"
}

resource "docker_image" "influxdb_image" {
    name = "influxdb:${var.image_version}"
}

resource "docker_container" "influxdb_container" {
    name = "${var.name_prefix}-influxdb_container"
    image = docker_image.influxdb_image.latest
    restart = "always"
    volumes {
        volume_name = docker_volume.influxdb_volume.name
        container_path = "/var/lib/db"
    }
    networks_advanced {
        name = var.backend_network_name
    }
    env = [
        "INFLUXDB_DB=${var.influxdb_dbname}",
        "INFLUXDB_USER=${var.influxdb_user}",
        "INFLUXDB_USER_password=${var.influxdb_password}"
    ] 
}

