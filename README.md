# WiFi Scanner

## Overview
WiFi Scanner is a desktop application developed in Python using PyQt5. It provides a simple and intuitive interface for scanning and connecting to WiFi networks. The application also includes a secure method for handling WiFi passwords and remembers previously connected networks for user convenience.

## Features
- **Scan WiFi Networks:** The application scans and displays available WiFi networks.
- **Connect to a Network:** Users can select a network from the list and connect to it by entering the password.
- **Secure Password Handling:** Passwords are securely hashed using SHA256 before being stored. The application remembers the passwords for previously connected networks, so users don't have to enter them again.
- **Connection Prompts:** The application uses `QMessageBox` prompts to notify users about the connection status.
- **Toggle WiFi:** A toggle button allows users to enable or disable WiFi scanning.

## Screenshots
Here are some screenshots of the application in action:

**WiFi Disabled:**
!WiFi Disabled

**WiFi Enabled and Connected:**
!WiFi Enabled and Connected

## Dependencies
- Python 3
- PyQt5

## How to Run
1. Clone the repository: `git clone YOUR_REPOSITORY_URL`
2. Navigate to the project directory: `cd YOUR_PROJECT_DIRECTORY`
3. Run the application: `python main.py`

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the terms of the MIT license.
