data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*"]
  }
}

resource "tls_private_key" "cipher" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "cipher" {
  key_name   = "${var.project}-prod-key"
  public_key = tls_private_key.cipher.public_key_openssh
}

resource "local_file" "private_key" {
  content         = tls_private_key.cipher.private_key_pem
  filename        = "${path.module}/cipher-prod-key.pem"
  file_permission = "0400"
}

resource "aws_iam_role" "ec2" {
  name = "${var.project}-ec2-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "s3" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "ecr" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project}-ec2-profile"
  role = aws_iam_role.ec2.name
}

resource "aws_instance" "cipher" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.ec2_instance_type
  key_name               = aws_key_pair.cipher.key_name
  subnet_id              = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name

  root_block_device {
    volume_size = 80
    volume_type = "gp3"
  }

  user_data = base64encode(file("${path.module}/userdata.sh"))
  tags      = { Name = "${var.project}-production" }
}

resource "aws_eip" "cipher" {
  instance = aws_instance.cipher.id
  domain   = "vpc"
  tags     = { Name = "${var.project}-eip" }
}
