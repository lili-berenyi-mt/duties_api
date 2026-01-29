terraform {
  required_version = "~> 1.14"
  backend "s3" {
    key = "app.tfstate"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 2"
    }

    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.2"
    }

    local = {
      source  = "hashicorp/local"
      version = ">= 2.6"
    }
  }
}

provider "aws" {
  default_tags {
    tags = {
      owner           = "lili"
      application     = "duties-api"
      managed-by      = "terraform"
      managed-by-repo = "@lili-berenyi-mt/duties_api"
    }
  }
}