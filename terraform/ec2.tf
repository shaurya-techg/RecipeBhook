data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

resource "aws_instance" "devsecops" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  key_name = "recipebhook-devsecops-key"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.devsecops.id
  ]

  associate_public_ip_address = true

  root_block_device {
    volume_size = 30
    volume_type = "gp3"

    encrypted = true
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_eip" "devsecops" {
  domain = "vpc"

  tags = {
    Name        = "${var.project_name}-${var.environment}-eip"
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
#elastic ip association with the instance
resource "aws_eip_association" "devsecops" {
  instance_id   = aws_instance.devsecops.id
  allocation_id = aws_eip.devsecops.id
}