import panel as pn
from clickhouse_driver import Client

# Create a ClickHouse client. We'll use the service name "clickhouse" from docker-compose
# for the host, and default port 9000 for native protocol.
client = Client(host='clickhouse', port=9000)

def fetch_data():
    """
    Simple function to query the first few numbers from the system.numbers table.
    This is built-in test data in ClickHouse.
    """
    query = "SELECT number FROM system.numbers LIMIT 5"
    result = client.execute(query)
    # Convert the tuple-list result into a more user-friendly list or DataFrame
    # For Panel display, we can just return a list of lists or a simple DataFrame
    return result

# Create a Panel object. 
# You can customize or build something more elaborate as needed.
data_view = pn.widgets.DataFrame(fetch_data(), name="ClickHouse Data")

# Serve the app
if __name__ == "__main__":
    pn.serve(data_view, port=80, address='0.0.0.0')