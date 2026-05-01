variable "aws_region" {
  default = "ap-south-1"
}

variable "project" {
  default = "cipher"
}

variable "environment" {
  default = "production"
}

variable "ec2_instance_type" {
  default = "t3.xlarge"
}

variable "db_instance_class" {
  default = "db.t3.micro"
}

variable "db_password" {
  description = "RDS master password"
  type        = string
  sensitive   = true
  default     = "cipher_prod_pass_change_me"
}
