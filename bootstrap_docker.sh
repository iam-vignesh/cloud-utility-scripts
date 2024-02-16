 #!/bin/bash

# Exit on errors
set -e

# Update package list
sudo apt update
if [ $? -ne 0 ]; then
  echo "Error: Failed to update package list!"
  exit 1
fi

# Install necessary packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common || {
  echo "Error: Failed to install required packages!"
  exit 1
}

# Add Docker repository key
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
if [ $? -ne 0 ]; then
  echo "Error: Downloading or importing Docker key failed!"
  exit 1
fi

# Add Docker repository
sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
if [ $? -ne 0 ]; then
  echo "Error: Adding Docker repository failed!"
  exit 1
fi

# Update package list
sudo apt update
if [ $? -ne 0 ]; then
  echo "Error: Failed to update package list after adding Docker repository!"
  exit 1
fi

# Install Docker
sudo apt install -y docker-ce || {
  echo "Error: Installing Docker failed!"
  exit 1
}

# Add current user to the docker group (optional)
# Check if already in group before attempting addition
if ! groups ${USER} | grep -q docker; then
  sudo usermod -aG docker ${USER} || {
    echo "Warning: Adding user to docker group failed!"
  }
fi

# Start Docker service
sudo systemctl start docker
if [ $? -ne 0 ]; then
  echo "Error: Starting Docker service failed!"
  exit 1
fi

echo "No errors detected during bootstraping Docker! Run 'systemctl status docker' to confirm status"
