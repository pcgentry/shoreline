module "sample_security_group" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "user-service"
  description = "Security group for user-service"
  vpc_id      = "vpc-12345678"

  ingress_with_cidr_blocks = [
    {
      from_port   = 8080
      to_port     = 8080
      protocol    = "tcp"
      description = "Internal Network"
      cidr_blocks = "10.10.10.0/24"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      description = "Seattle Office Vpn"
      cidr_blocks = "72.172.213.172/32"
    }
  ]
}
