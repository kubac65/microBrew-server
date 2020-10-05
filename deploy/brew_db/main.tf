resource "docker_volume" "couchdb_volume" {
    name = "${var.name_prefix}-couchdb_volume"
}

resource "docker_image" "couchdb_image" {
    name = "bitnami/couchdb:${var.image_version}"
}

resource "docker_container" "couchdb_container" {
    name = "${var.name_prefix}-couchdb_container"
    image = docker_image.couchdb_image.latest
    restart = "always"
    volumes {
        volume_name = docker_volume.couchdb_volume.name
        container_path = "/bitnami/couchdb"
    }
    networks_advanced {
        name = var.backend_network_name
    }
    env = [
        "COUCHDB_USER=${var.couchdb_user}",
        "COUCHDB_PASSWORD=${var.couchdb_password}"
    ]
}