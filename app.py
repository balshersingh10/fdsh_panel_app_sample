import panel as pn
import clickhouse_connect

# Create a label widget to display messages
label = pn.pane.Markdown("Click the button to do something!")

# Define a callback function to run when the button is clicked
def on_button_click(event):
    label.object = "Button clicked!"

# Create a button and link it to the callback
button = pn.widgets.Button(name="Click Me", button_type="primary")
button.on_click(on_button_click)

# Build the layout (for instance, a vertical Column)
layout = pn.Column(
    "# My Simple Panel App",
    "This is a static page with a single button.",
    button,
    label
)

if __name__ == "__main__":
    # Serve the layout on port 80 by default
    # Or specify another port if you like (e.g., port=8080)
    pn.serve(layout, port=80, address="0.0.0.0")
