provider "aws" {
    region="eu-north-1"
}

variable "docker_username" {
  type        = string
  description = "DockerHub username"
  sensitive = true
}

variable "database_url" {
  type        = string
  description = "Connection string for the database"
  sensitive   = true
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
  owners = ["099720109477"]
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "./.ssh/terraform_rsa"
}

resource "local_file" "public_key" {
  content  = tls_private_key.ssh_key.public_key_openssh
  filename = "./.ssh/terraform_rsa.pub"
}

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = "subnet-ba3fc8d3"
  vpc_security_group_ids = ["sg-0d951b9dddd0a3768"]
  key_name               = "terraform-key"
  user_data = templatefile("${path.module}/cloud-init.yml.tmpl", {
    instance_name = "duties-api-lili"
    docker_username = var.docker_username
    database_url    = var.database_url
  })
  tags = {
    Name = "duties_api_lili"
  }
}

output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value = aws_instance.app_server.public_ip
}