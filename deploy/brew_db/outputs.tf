output "host" {
    value = docker_container.couchdb_container.name
}

output "port" {
    value = 5984
}