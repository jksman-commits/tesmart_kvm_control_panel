# tesmart_kvm_control_panel
Web-based control panel for managing Tesmart 8x1 HDMI KVM switch via a simple interface.
# Tesmart 8x1 HDMI KVM Switch Control Panel

![Docker](https://img.shields.io/docker/pulls/jksman/tesmart_kvm_control_panel) ![GitHub issues](https://img.shields.io/github/issues/jksman-commits/tesmart_kvm_control_panel)

## Overview

This project provides a web-based control panel for managing the **Tesmart 8x1 HDMI KVM Switch**. The application allows users to easily switch between up to 8 connected computers via an intuitive web interface. Built with Flask and packaged in a Docker container, this tool streamlines the management of your KVM switch from any device with a browser.

## Features

- **Web-based Control**: Manage and switch between 8 connected computers using a simple web interface.
- **Dockerized**: Easily deployable in any environment using Docker.
- **Customizable**: Configuration options available for setting up the KVM IP and port.

## Prerequisites

- **Tesmart 8x1 HDMI KVM Switch**
- **Docker Installed** on the host machine

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jksman-commits/tesmart_kvm_control_panel.git
cd tesmart_kvm_control_panel
2. Build and Run the Docker Container
Build the Docker image:

bash
Copy code
docker build -t jksman/tesmart_kvm_control_panel:latest .
Run the Docker container:

bash
Copy code
docker run -p 9090:9090 -v ~/config_data:/config jksman/tesmart_kvm_control_panel:latest
This will start the control panel on port 9090. You can access the control panel via http://localhost:9090 or http://<host-ip>:9090.

3. Configuration
The configuration file (config.json) will be created in the /config directory. Make sure to mount a local directory to /config so that your configuration persists between runs.

4. Usage
Open your browser and navigate to http://localhost:9090.
Switch between the connected PCs using the web interface by clicking on the respective buttons for PC1 through PC8.
5. Automated Builds
This repository is linked to Docker Hub and is automatically built whenever changes are pushed to GitHub. You can also pull the pre-built image from Docker Hub:

docker pull jksman/tesmart_kvm_control_panel:latest
Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add a new feature').
Push to the branch (git push origin feature-branch).
Create a pull request.

Issues
Feel free to open issues if you encounter any problems or have questions regarding the project.

Acknowledgments
Tesmart: For the 8x1 HDMI KVM Switch that this project supports.
Flask: For providing a simple and powerful web framework.
Author
jksman

Find me on GitHub and Docker Hub.
