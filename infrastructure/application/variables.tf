variable "docker_username" {
  type        = string
  description = "DockerHub username"
  sensitive   = true
}

variable "database_url" {
  type        = string
  description = "Connection string for the database"
  sensitive   = true
}