# Simple GPS data simulator

## Description

This is a simple data generator mocking a GPGGA data source. The datasource is then proccessed to an kafka-server (`hiwi-test-kafka-1:29092`)

## Task
Please provide a service that subscribes to the Kafka topic `location_topic` and visualize the data on a map. A containerized solution is preferred. You may extend the service to provide additional features like filtering, some additional visualization, etc. You may use any programming language, any framework, or any library. 

AC:
* [ ] The service needs to use the data from the kafka topic `location_topic`
* [ ] The service should decode the protobuf data messages 
* [ ] The service should be able to visualize the data on a map
* [ ] The service should be containerized

Question to be answered:
* What object can be expected to move with that trajectory?

## Installation

### Building the project

* Dependencies
  * docker
  * protobuf (for decoding the data)

* Building the project:

```
docker compose up -d
```

### Usage

* For a better interaction with docker you can use the VSCode docker extension: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker

* If the docker containers are running, you may find the kafka-UI (kafka-drop) at [http://localhost:9000/](http://localhost:9000/)


### Protobuf

* Install protobuf

```
sudo apt install -y kafkacat protobuf-compiler
```

* Generating python descriptors

```
protoc -I="." --python_out=src/gen ./location.proto
```

* Generating kafkadrop descriptors (Ubuntu)

```
protoc -o descriptors/location.desc location.proto
```

### Known issues
* Error while running the kafka broker (i.e. `unable to allocate file descriptor table - out of memory`):
-> Solution: as often can provide [stackoverflow](https://stackoverflow.com/questions/68776387/docker-library-initialization-failed-unable-to-allocate-file-descriptor-tabl)

(!) Please open an issue if you find any problems.


# Location Service Documentation

## Overview

The Location Service is designed to consume and visualize real-time data from the Kafka topic `location_topic`. The data, encoded in Protobuf format, contains information such as UTC time, latitude, longitude, and more.

## Service Features

1. **Kafka Topic Consumption**
   - Utilizes the `confluent_kafka` library to create a Kafka consumer.
   - Configures the consumer with bootstrap servers, group ID, and subscribes to the `location_topic`.

2. **Dash App and Plotly Map Initialization**
   - Hosts an interactive map visualization using Dash and Plotly Express.
   - Initializes an empty scatter map with an OpenStreetMap style.
   - Implements layout components with a graph for the map and an interval for periodic updates.

3. **Protobuf Data Structure**
   - Adheres to the Protobuf schema defined in `location.proto`.
   - Fields include UTC time, latitude, longitude, quality, number of satellites, HDOP, altitude, and more.

4. **Protobuf Deserialization**
   - Deserializes the protobuf data received from Kafka using `location.ParseFromString()`.
   - Extracts relevant information from the protobuf message for visualization.

5. **Location Data Formatting Function**
   - Implements `format_location_data` to format latitude and longitude data according to the `location.proto` specifications.
   - Returns formatted latitude and longitude strings.

6. **Dynamic Dash Callback for Real-time Plotting**
   - Modifies the Dash callback to dynamically update the map with real-time location data.
   - Utilizes the formatted latitude and longitude data in the callback.

7. **Docker Containerization**
   - Provides Dockerfile for containerization.
   - Includes build instructions and necessary environment variables or configurations.

8. **Documentation for Service Usage**
   - Documents steps to access the Kafka topic, decode protobuf data, and visualize data on the map.
   - Offers deployment instructions, including details on deploying the Dockerized service.

9. **Acknowledged Real-time Plotting Issues**
   - Explicitly acknowledges the current limitation in real-time data plotting.
   - Describes any known issues preventing dynamic map updates.

10. **Additional Notes**
    - Includes any additional information, potential improvements, or troubleshooting tips for users.

## Steps to Create the Final Script

### 1. Set up Kafka Consumer
   - Use the `confluent_kafka` library to create a Kafka consumer.
   - Configure the consumer with appropriate bootstrap servers, group ID, and topic.
   - Subscribe to the `location_topic` Kafka topic.

### 2. Initialize Dash App and Plotly Map
   - Create a Dash app to host the live map visualization at ``` localhost:8000```
   - Use Plotly Express to initialize an empty scatter map with an OpenStreetMap style.
   - Set up the layout of the Dash app with a graph component for the map and an interval component for periodic updates.

### 3. Define Protobuf Message Structure
   - Define the protobuf message structure using the provided `location.proto` file.
   - Include fields for UTC time, latitude, longitude, quality, number of satellites, HDOP, altitude, undulation, age, and station ID.

### 4. Implement Protobuf Deserialization
   - Deserialize the protobuf data received from Kafka using the `location.ParseFromString()` method.
   - Extract relevant information from the protobuf message for visualization.

### 5. Create Location Data Formatting Function
   - Implement a function (`format_location_data`) to format latitude and longitude data according to the specified format in the `location.proto` file.
   - The function returns formatted latitude and longitude strings.

### 6. Update Dash Callback for Real-time Plotting
   - Modify the Dash callback to dynamically update the map with real-time location data.
   - Use the formatted latitude and longitude data in the callback.

### 7. Set Up Docker Containerization
   - Create a Dockerfile to containerize the service.
   - Include instructions to build the Docker image.
   - Specify any necessary environment variables or configurations.

### 8. Document the Service
   - Document the steps to access the Kafka topic, decode protobuf data, and visualize the data on the map.
   - Provide deployment instructions, including details on deploying the Dockerized service.

### 9. Acknowledge Real-time Plotting Issues
   - Explicitly mention the current limitation in real-time data plotting.
   - Describe any known issues preventing dynamic map updates.

By following these steps, the final script should be able to consume, decode, and visualize real-time location data from the specified Kafka topic.




