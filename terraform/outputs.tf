output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "DevSecOps security group ID"
  value       = aws_security_group.devsecops.id
}

output "availability_zone" {
  description = "Availability zone"
  value       = data.aws_availability_zones.available.names[0]
}

output "instance_id" {
  description = "DevSecOps EC2 instance ID"
  value       = aws_instance.devsecops.id
}

output "public_ip" {
  description = "DevSecOps EC2 public IP"
  value       = aws_instance.devsecops.public_ip
}

output "public_dns" {
  description = "DevSecOps EC2 public DNS"
  value       = aws_instance.devsecops.public_dns
}

output "elastic_ip" {
  description = "Elastic IP address of the DevSecOps server"
  value       = aws_eip.devsecops.public_ip
}