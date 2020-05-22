# Irrigation System

Sends data to an MQTT connection.

## Setup

### Requirements

Python3, pip3, screen (and probably other stuff...) needs to be installed on your Raspberry Pi.

### Environment variables

Add an `.env`-file to the root of the project to set environment variables (see `.env.example`).

## Usage

There are some handy shortcuts in the `scripts`-folder:

* `sh ./scripts/setup.sh` — install python dependencies

To run tests, give the name of the test-file as an argument:

* `sh ./scripts/test.sh mqtt` — runs `./tests/mqtt.py`
* `sh ./scripts/test.sh AM2320` — runs `./tests/AM2320.py`
* ... and so on

Note: running tests also kills main thread.

## API

Each device publishes values on its own topic in the following format:

```
{
  "humidity": 98.0,
  "temperature": 20.1
}
```
