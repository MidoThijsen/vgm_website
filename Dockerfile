# Use the Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies for Chrome and ChromeDriver
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
    chromium-driver

# # Optional: Install a specific version of Google Chrome (v114.0.5735.90)
# RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get update && apt-get install -y google-chrome-stable=114.0.5735.90-1

# # Optional: Install a specific version of ChromeDriver (v114.0.5735.90)
# RUN wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip && \
#     mv chromedriver /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver

# Copy the current directory contents into the container
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the required Python packages (including selenium)
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "./main.py"]
