# main.tf

# Configure AWS provider
provider "aws" {
  region = "us-east-1"  # Update with your desired region
}

resource "aws_security_group" "ssh_sg" {
  name        = "ssh-security-group"
  description = "Allow SSH inbound traffic"

  # Allow inbound SSH traffic from all sources (0.0.0.0/0)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_key_pair" "api-server-key-v2" {
  key_name = "api-server-key-v2"  # Replace with your existing key pair name
}


# Define EC2 instance
resource "aws_instance" "tf-instance" {
  ami           = "ami-06aa3f7caf3a30282"  # Example AMI, update with your desired AMI
  instance_type = "t2.micro"               # Instance type

  tags = {
    Name = "tf-instance-1"
  }

  security_groups = [aws_security_group.ssh_sg.name]

  key_name = data.aws_key_pair.api-server-key-v2.key_name

  # Define connection block for remote-exec provisioner
  connection {
    type        = "ssh"
    user        = "ubuntu"  # Update with the appropriate user for your AMI
    private_key = file("~/.ssh/prod-server.pem")  # Update the path to your private key
    host        = self.public_ip
  }

  # Define provisioner to upload and execute script remotely
  provisioner "remote-exec" {
    # Path to the local script
    script = "/home/vignesh/bootstrap_docker.sh"
  }
}

# Output the public IP address of the instance
output "instance_public_ip" {
  value = aws_instance.tf-instance.public_ip
}
