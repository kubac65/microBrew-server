output "host" {
    value = docker_container.influxdb_container.name
}

output "port" {
    value = 8086
}