from confluent_kafka import Consumer, KafkaError
from gen import location_pb2
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Kafka broker configuration
bootstrap_servers = 'kafka:9092'
group_id = 'visualizer'
topic = 'location_topic'

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([topic])

location = location_pb2.location()  # Create a position instance

# Function to format location data
def format_location_data(location):
    formatted_lat = f"{location.latitude} {location.lat_direction}"
    formatted_lon = f"{location.longitude} {location.lon_direction}"
    formatted_data = (
        f"UTC Time: {location.utc_time}\n"
        f"Latitude: {formatted_lat}\n"
        f"Longitude: {formatted_lon}\n"
        f"Quality: {location.quality}\n"
        f"Number of Satellites: {location.num_sats}\n"
        f"HDOP: {location.hdop}\n"
        f"Altitude: {location.altitude} {location.alt_units}\n"
        f"Undulation: {location.undulation} {location.und_units}\n"
        f"Age: {location.age}\n"
        f"Station ID: {location.stn_id}"
    )
    return formatted_data

# Initialize Dash app
app = dash.Dash(__name__)

# Create initial figure with an overview of Europe
initial_fig = go.Figure(go.Scattermapbox(
    lat=[],
    lon=[],
    mode='markers',
    marker=dict(size=9),
    text=[],
))

initial_fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        zoom=3,  # Set initial zoom level for an overview of Europe
        center=dict(lat=51.1657, lon=10.4515),  # Centered around Europe
    ),
)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='live-update-graph', figure=initial_fig),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='live-update-text')  # Div for displaying received data
])

# Callback to update the graph and display received data
@app.callback([Output('live-update-graph', 'figure'),
               Output('live-update-text', 'children')],
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    msg = consumer.poll(1.0)

    if msg is None:
        return initial_fig, "No data received"

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition {msg.partition()}")
        else:
            print(f"Error: {msg.error()}")
    else:
        # Deserialization of the protobuf data
        location.ParseFromString(msg.value())

        # Format the location data
        formatted_data = format_location_data(location)

        # Print formatted data in the shell
        print(formatted_data)

        # Update the figure with the received point
        updated_fig = go.Figure(go.Scattermapbox(
            lat=[float(location.latitude)],
            lon=[float(location.longitude)],
            mode='markers',
            marker=dict(size=9),
            text=[f'Timestamp: {location.utc_time}'],
        ))

        updated_fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                zoom=3,  # Keep the initial zoom level for an overview of Europe
                center=dict(lat=51.1657, lon=10.4515),  # Centered around Europe
            ),
        )

        # Display received data in the dashboard
        return updated_fig, formatted_data


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8000)
