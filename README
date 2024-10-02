This is a placeholder for our project. I will add a description of the project as we go. (Example change)


# Greenhouse IoT Project - Tech Stack Overview

## Tech Stack Overview

The Greenhouse IoT project is built using a combination of modern technologies to create a user-friendly, responsive system for automating greenhouse management. The project involves both hardware (sensors and actuators) and software (user interface and backend logic). Below is an overview of the key technologies and frameworks used:

### 1. Python (Backend Logic and Sensors Control)

We use Python as the primary language to manage communication with sensors and actuators, perform environmental monitoring, and control the system’s logic. Python’s simplicity and rich ecosystem make it ideal for interacting with hardware and processing real-time data.

- **Libraries**:
  - `pyserial`: For communicating with the Arduino co-processor.
  - `kivy`: For building the graphical user interface (GUI).
  - `time`: For event loops and delays in real-time data processing.

### 2. Kivy (Graphical User Interface)

Kivy is used to create a cross-platform GUI that allows the user to manage the greenhouse system easily. The interface supports touchscreen interactions and runs on Linux, providing real-time control over the greenhouse environment (adding plants, removing plants, monitoring sensors).

- **Features**:
  - Touch-friendly UI
  - Buttons for adding/removing plants, checking status, and managing settings
  - Custom theming (green and white) to match the greenhouse environment

### 3. LattePanda Sigma / Raspberry Pi 5 (Development Board)

The project is built on either the **LattePanda Sigma** or **Raspberry Pi 5** development board, which provides the processing power and GPIO access required for managing sensors and actuators. The boards also run Linux, making it easy to interface with Python and Kivy for running the software continuously.

- **LattePanda Sigma**: Ideal for Windows-based remote development and testing.
- **Raspberry Pi 5**: A powerful, Linux-based board for embedded systems development.

### 4. Systemd (For Continuous Running and Startup)

The software is configured to run as a service using `systemd`, ensuring that the program automatically starts when the device boots and runs continuously without manual intervention. This ensures that the greenhouse system can operate 24/7.

- **`systemd`** service ensures:
  - Automatic startup on boot
  - Restart on failure or crashes

---

## Setup Instructions for Development

If you're a new developer joining the project, follow the steps below to set up the development environment and run the software.

### 1. Clone the Repository

First, clone the project repository:

```bash
git clone https://github.com/your-organization/greenhouse-iot-project.git
cd greenhouse-iot-project
``` 

### 2. Set Up Python Virtual Environment

It’s recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

Once your virtual environment is activated, install the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install the necessary libraries, including kivy, pyserial, and others required for the project.

### 4. Set Up the Development Board

Ensure you have the required development board (LattePanda Sigma or Raspberry Pi 5) connected to your machine. The system will communicate with the sensors and actuators through the board’s GPIO pins or the Arduino co-processor.

For LattePanda:

- Ensure Windows/Linux is installed and running.
- Set up the Arduino IDE for microcontroller communication.

For Raspberry Pi:

- Ensure Linux is installed.
- Access the GPIO pins to connect the sensors and actuators.

### 5. Set Up ```systemd``` for Automatic Startup (Optional)

To make the software run continuously on startup, configure the project to run as a systemd service. Follow these steps:

1. Create a new service file:

```bash
sudo nano /etc/systemd/system/greenhouse.service
```
2. Add the following content:
```ini
[Unit]
Description=Greenhouse IoT Software
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/main.py
WorkingDirectory=/path/to/your/project
Restart=always
User=your-username

[Install]
WantedBy=multi-user.target
```

3. Enable the service:

```bash
sudo systemctl enable greenhouse.service
sudo systemctl start greenhouse.service
```
This ensures the software starts automatically on boot and restarts on failure.

### 6. Run the Software

Finally, run the software using the following command:

```bash
python main.py
```

This will launch the GUI interface, allowing you to interact with the system, monitor the sensors, and manage the greenhouse environment.

If you would like to contribute, please submit a pull request or reach out to the team for guidance on implementing new features or fixing bugs. Ensure you are following the project's coding standards and have tested your code before submission.
