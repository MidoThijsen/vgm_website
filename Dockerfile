# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies for Chrome and ChromeDriver (optional for Selenium usage)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg2 \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    xdg-utils \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libgbm-dev \
    libgtk-3-0 \
    libnspr4 \
    libpango1.0-0 \
    libcups2 \
    libxss1 \
    libasound2 \
    lsb-release \
    libu2f-udev \
    chromium \
    chromium-driver \
    openssh-server  # Install OpenSSH server

# Configure SSH: Set root password and ensure SSH service can start
RUN echo 'root:Docker!' | chpasswd && mkdir /var/run/sshd

# Expose SSH port 2222
EXPOSE 2222

# Copy the current directory contents into the container
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the required Python packages (including Flask and selenium if required)
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Expose port 5000 for Flask
EXPOSE 5000

# Start SSH service and the Flask app
CMD service ssh start && flask run --host=0.0.0.0 --port=5000
