import panel as pn
import pandas as pd
import clickhouse_connect

# Connect to ClickHouse (adjust host, port, user, password as needed)
client = clickhouse_connect.get_client(
    host="clickhouse",
    port=8123,
    username="admin",
    password="ggf_db"
)

# We'll store messages and data in these panel components
status_message = pn.pane.Markdown("")
data_table = pn.widgets.DataFrame(pd.DataFrame(), name="ClickHouse Data")

def create_table(event):
    """
    Creates a simple table if it doesn't exist.
    """
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS my_demo (
            id UInt64,
            name String,
            dt DateTime
        ) 
        ENGINE = MergeTree()
        ORDER BY id
        """
        client.command(create_query)
        status_message.object = "**Table created or already exists.**"
    except Exception as e:
        status_message.object = f"**Error creating table**: {str(e)}"

def insert_data(event):
    """
    Inserts some dummy records into the table.
    """
    try:
        # Inserting multiple rows; the clickhouse_driver can handle a list of tuples
        data = [
            (1, "Alice", "2025-01-01 10:00:00"),
            (2, "Bob",   "2025-01-01 11:00:00"),
            (3, "Charlie","2025-01-01 12:00:00")
        ]
        df = pd.DataFrame(data,columns=['id','name','dt'])
        df['dt'] = pd.to_datetime(df['dt'])
        # Format: "INSERT INTO table VALUES", then pass parameters
        client.insert_df('my_demo', df)
        status_message.object = "**Inserted 3 rows of dummy data.**"
    except Exception as e:
        status_message.object = f"**Error inserting data**: {str(e)}"

def show_data(event):
    """
    Fetches data from the table and displays it in a Panel DataFrame widget.
    """
    try:
        query = """SELECT "id", "name", "dt" FROM my_demo"""
        df = client.query_df(query)
        data_table.value = df
        status_message.object = "**Showing up to 50 rows**"
    except Exception as e:
        status_message.object = f"**Error fetching data**: {str(e)}"
        data_table.value = pd.DataFrame()  # clear table

# Create the buttons
create_button = pn.widgets.Button(name="Create Table", button_type="primary")
create_button.on_click(create_table)

insert_button = pn.widgets.Button(name="Insert Data", button_type="success")
insert_button.on_click(insert_data)

show_button = pn.widgets.Button(name="Show Data", button_type="warning")
show_button.on_click(show_data)

# Layout
app_layout = pn.Column(
    "# Simple ClickHouse Demo",
    "Use the buttons below to create a table, insert data, and show data.",
    create_button,
    insert_button,
    show_button,
    status_message,
    data_table
)

if __name__ == "__main__":
    pn.serve(app_layout, address="0.0.0.0", port=80)