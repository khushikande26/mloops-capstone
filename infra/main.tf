provider "aws" {
  region = "us-east-1"   # change if you want to deploy in another region
}

resource "aws_instance" "fastapi_server" {
  ami           = "ami-08982f1c5bf93d976" # Ubuntu 22.04 LTS AMI (make sure it's valid in your region)
  instance_type = "t3.micro"
  key_name      = var.key_name             # your EC2 key pair name

  # Attach your existing security group
  vpc_security_group_ids = ["sg-0914ec2d4e4c0bbb1"]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker

              # pull & run FastAPI container
              docker run -d -p 80:8000 ${var.docker_image}
              EOF

  tags = {
    Name = "fastapi-mloops"
  }
}
