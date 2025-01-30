import panel as pn
import pandas as pd
import clickhouse_connect
import traceback

# Connect to ClickHouse (adjust host, port, user, password as needed)
client = clickhouse_connect.get_client(
    host="clickhouse",
    username="admin",
    password="ggf_db",
)

# We'll store messages and data in these panel components
status_message = pn.pane.Markdown("")
data_table = pn.widgets.DataFrame(pd.DataFrame(), name="ClickHouse Data")

def create_table(event):
    """
    Creates a simple table if it doesn't exist, then verifies it's created.
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

        # Check if table is indeed created
        check_query = "EXISTS TABLE my_demo"
        result = client.command(check_query)
        # ClickHouse returns 1 if table exists, 0 otherwise
        if result == 1:
            # (Optional) show the schema
            schema_info = client.command("SHOW CREATE TABLE my_demo")
            status_message.object = (
                "**Table created or already exists.**\n\n"
                f"```sql\n{schema_info}\n```"
            )
        else:
            status_message.object = (
                "**Table creation attempted, but table not found.**"
            )
    except Exception as e:
        # For more detailed stack trace, gather it
        err_trace = traceback.format_exc()
        status_message.object = f"**Error creating table**:\n```\n{str(e)}\n\n{err_trace}\n```"

def insert_data(event):
    """
    Inserts some dummy records into the table.
    """
    try:
        # Prepare a small DataFrame
        # data = [
        #     (1, "Alice",   "2025-01-01 10:00:00"),
        #     (2, "Bob",     "2025-01-01 11:00:00"),
        #     (3, "Charlie", "2025-01-01 12:00:00")
        # ]
        # df = pd.DataFrame(data, columns=['id','name','dt'])
        # df['dt'] = pd.to_datetime(df['dt'])  # ensure datetime type

        # # Use clickhouse_connect insert_df
        # client.insert_df('my_demo', df)
        client = clickhouse_connect.get_client(
            host="clickhouse",
            username="admin",
            password="ggf_db",
        )
        client.command("INSERT INTO my_demo (id, name) VALUES (1, 'Tangs')")
        status_message.object = "**Inserted 1 rows of dummy data.**"
    except Exception as e:
        err_trace = traceback.format_exc()
        status_message.object = f"**Error inserting data**:\n```\n{str(e)}\n\n{err_trace}\n```"

def show_data(event):
    """
    Fetches data from the table and displays it in a Panel DataFrame widget.
    """
    try:
        query = "SELECT id, name, dt FROM my_demo ORDER BY id LIMIT 50"
        df = client.query_df(query)
        data_table.value = df
        status_message.object = (
            f"**Showing {len(df)} rows (up to 50).**"
            if not df.empty else
            "**Table is empty or not found.**"
        )
    except Exception as e:
        err_trace = traceback.format_exc()
        status_message.object = f"**Error fetching data**:\n```\n{str(e)}\n\n{err_trace}\n```"
        data_table.value = pd.DataFrame()  # clear table

def drop_table(event):
    """
    Drops the 'my_demo' table if it exists, clearing out all data.
    """
    try:
        drop_query = "DROP TABLE IF EXISTS my_demo"
        client.command(drop_query)
        status_message.object = "**Table 'my_demo' has been dropped.**"
        # Clear out any displayed data
        data_table.value = pd.DataFrame()
    except Exception as e:
        err_trace = traceback.format_exc()
        status_message.object = f"**Error dropping table**:\n```\n{str(e)}\n\n{err_trace}\n```"

# Create buttons
create_button = pn.widgets.Button(name="Create Table", button_type="primary")
create_button.on_click(create_table)

insert_button = pn.widgets.Button(name="Insert Data", button_type="success")
insert_button.on_click(insert_data)

show_button = pn.widgets.Button(name="Show Data", button_type="warning")
show_button.on_click(show_data)

drop_button = pn.widgets.Button(name="Delete Table", button_type="danger")
drop_button.on_click(drop_table)

# Build the Panel layout
app_layout = pn.Column(
    "# Simple ClickHouse Demo V1",
    "Use the buttons below to create a table, insert data, and show data.",
    create_button,
    insert_button,
    show_button,
    drop_button,
    status_message,
    data_table
)

if __name__ == "__main__":
    # If you need to allow external hostnames, specify them below
    pn.serve(
        app_layout,
        address="0.0.0.0",
        port=80,
        allow_websocket_origin=["*"]  # or your domain
    )
