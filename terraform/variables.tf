variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "recipebhook"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "devsecops"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "m7i-flex.large"
}