import time
from datetime import datetime, timezone
from confluent_kafka import Producer
from gen import location_pb2  # Import the generated Protobuf module

kafka_on = True

# Delivery report for Kafka
def delivery_report(err, msg):
    """Delivery callback for Kafka produce."""
    if err is not None:
        print(f'Message delivery to Kafka failed: {err}')
    else:
        print(f'Message delivered to Kafka to {msg.topic()} [{msg.partition()}]')

# Kafka broker configuration
if kafka_on:
    bootstrap_servers = 'kafka:9092'  # Use the Kafka bootstrap servers specified in docker-compose.yml
    producer = Producer({'bootstrap.servers': bootstrap_servers,
                         'message.max.bytes': 209715200})  # Create a Kafka producer

location = location_pb2.location()  # Create a position instance

while True:
    file_path = './src/source_stream.txt'  # Use the correct file path
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            data_fields = line.strip().split(",")
            
            if data_fields[0] == '$GPGGA':
                print(data_fields)
                
                location.utc_time = datetime.now(timezone.utc).timestamp()
                location.latitude = data_fields[2]
                location.lat_direction = data_fields[3]
                location.longitude = data_fields[4]
                location.lon_direction = data_fields[5]
                location.quality = int(data_fields[6])
                location.num_sats = int(data_fields[7])
                location.hdop = float(data_fields[8])
                location.altitude = float(data_fields[9])
                location.alt_units = data_fields[10]
                location.undulation = float(data_fields[11])
                location.und_units = data_fields[12]
                location.age = 0 if data_fields[13] == "" else float(data_fields[13])
                location.stn_id = data_fields[14]

                if kafka_on:
                    # Send the extracted fields to Kafka
                    serialized_location = location.SerializeToString()
                    topic = 'location_topic'
                    producer.produce(topic=topic, key="rover", value=serialized_location, callback=delivery_report)
                    producer.flush()  # Flush messages and close producer

                time.sleep(1)

        time.sleep(1)
