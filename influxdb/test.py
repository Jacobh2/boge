from influxdb_client import InfluxDBClient, Point, WriteOptions

# Define your InfluxDB connection parameters
url = "http://192.168.1.220:8086"
# token = "your-token"
org = "home_assistant"
bucket = "home_assistant"

# Initialize the InfluxDB client
client = InfluxDBClient(
    url=url, username="sensors", password="sensorssensorssensors", org=org
)

# Define the query to list all measurements
query = f'from(bucket:"{bucket}") |> range(start: 0)'

# Execute the query
query_api = client.query_api()
result = query_api.query(org=org, query=query)

print("result:", result)

# Extract and print the measurements
measurements = result.keys["_value"]
print("Measurements:")
for measurement in measurements:
    print(measurement)
