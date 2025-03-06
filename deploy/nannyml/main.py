from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
import random

app = FastAPI()


def generate_figure():
    fig = go.Figure(data=[go.Scatter(y=[random.randint(0, 10) for _ in range(10)])])
    fig.update_layout(title="Live Updating Plotly Graph")
    return fig.to_html(full_html=False)

@app.get("/", response_class=HTMLResponse)
def index():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://unpkg.com/htmx.org@1.9.4"></script>
    </head>
    <body>
        <div id="graph-container" hx-get="/update_data" hx-trigger="every 2s"></div>
    </body>
    </html>
    """

@app.get("/update_data", response_class=HTMLResponse)
def update_data():
    return generate_figure()
