from confluent_kafka import Consumer, KafkaError
from gen import location_pb2
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

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

# Initialize Dash app
app = dash.Dash(__name__)

# Create initial figure with an overview of Europe
initial_fig = px.scatter_mapbox(
    lat=[],
    lon=[],
    text=[],
    zoom=3,  # Set initial zoom level for an overview of Europe
)
initial_fig.update_layout(mapbox_style="open-street-map")

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='live-update-graph', figure=initial_fig),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    msg = consumer.poll(1.0)

    if msg is None:
        return initial_fig

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition {msg.partition()}")
        else:
            print(f"Error: {msg.error()}")
    else:
        # Deserialization of the protobuf data
        location.ParseFromString(msg.value())

        # Print received data in the shell
        print(f"Timestamp: {location.utc_time}, Latitude: {float(location.latitude)} Longitude: {float(location.longitude)}")

        # Update the figure with the received point
        updated_fig = initial_fig.add_trace(
            px.scatter_mapbox(
                lat=[float(location.latitude)],
                lon=[float(location.longitude)],
                text=[f'Timestamp: {location.utc_time}'],
                zoom=3,  # Keep the initial zoom level for an overview of Europe
            ).data[0]
        )

        return updated_fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8000)
