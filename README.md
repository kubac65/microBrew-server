# microBrew-server
> Homebrew done the smart way

Brewing beer at home is a really cool hobby. Sometimes, it can be a bit tedious, but nothing can compete with the taste of the beer that you brewed yourself.

To help myself with this task, I'm building a **microBrew** suite that will help me to automate some of the tasks, and hopefully make the whole process a bit easier.

This project containe the source code for the server used for temperature monitoring and heating element control. It communicates with **microBrew-controller** using very simple text based protocol.

## Getting Started

### Installing Dependencies
Before you can get started with development, you need to make sure that all prerequisites are installed on your system. Project uses **InfluxDB** for recording temperatures, and **CouchDB** for storing brew batch metadata and recipes in the future. Those can be either installed on your system or run inside Docker container using provided `docker-compose.yml` file.

Next, create Python virtual environment that will be used for development, and install required dependencies:

```bash
# Create virtual environment
virtualenv venv

# Activate virtual environment
venv/Scripts/activate.sh # linux
# or
venv\Scripts\activate.bat # windows

# Finally install dependencies
pip install requirements.txt
```

### Initial Setup

Server reads its configuration from environment variables. All of the variables listed below, need to be set up on your dev machine before running the server. Take a look at `docker-compose.yml` to see how those are configured in docker environment.

| Variable Name  | Description            |
| -------------- | ---------------------- |
| TS_DB_HOST     | InfluxDB hostname      |
| TS_DB_PORT     | InfluxDB port          |
| TS_DB_USERNAME | InfluxDB username      |
| TS_DB_PASSWORD | InfluxDB password      |
| TS_DB_DATABASE | IndluxDB database name |
| BR_DB_HOST     | CouchDB hostname       |
| BR_DB_PORT     | CouchDB port           |
| BR_DB_USERNAME | CouchDB username       |
| BR_DB_PASSWORD | CouchDB password       |
| BR_DB_DATABASE | CouchDB database name  |
