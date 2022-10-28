resource "docker_container" "multichain-explorer-2" {
  image = "multichain-explorer-2:latest"
  name  = "multichain-explorer-2"
  restart = "always"
  volumes {
    container_path  = "/dashboard"
    # replace the host_path with full path for your project directory starting from root directory /
    host_path = "/dashboard" 
    read_only = false
  }
  ports {
    internal = 9090
    external = 9090
  }
}