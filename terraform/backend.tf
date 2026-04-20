terraform {
  backend "s3" {
    bucket = "kaltun-terraform-state"
    key    = "portfolio/terraform.tfstate"
    region = "eu-west-2"
  }
}