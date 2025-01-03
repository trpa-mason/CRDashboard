from datetime import datetime, timedelta
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import pathlib

from ClimateResilienceDashboard.utils import utils

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@custom
def plot_lake_level_with_high_water_mark(df):
    # Define the output directory (use a relative path if you're inside the container)
    # This will use the "html" folder from the local mounted volume in Docker
    html_path = pathlib.Path("/app/output")  # Path relative to the container

    # Ensure the output directory exists (this creates it if it doesn't exist)
    html_path.mkdir(parents=True, exist_ok=True)

    # Define the path for the output HTML file
    path_html = html_path / "1.3.a_Lake_Level.html"
    
    div_id = "1.3.a_Lake_Level"
    x = "dateTime"
    y = "value"
    color = None
    color_sequence = ["#023f64"]
    sort = "dateTime"
    orders = None
    x_title = "Date"
    y_title = "Water Level (feet)"
    hovertemplate = "%{y:,.0f} ft"
    format = ",.0f"
    tickvals = None
    ticktext = None
    tickangle = None
    hovermode = "x unified"
    
    # Sort the dataframe
    df = df.sort_values(by=sort)
    
    # Create a Plotly figure
    fig = go.Figure()

    # Add water level trace
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            name="Water Level",
            line=dict(color="#023f64"),
        )
    )

    # Define field/value for high water mark and low water mark
    df["High Water Mark"] = 6229
    df["Low Water Mark"] = 6223

    # Add high water mark trace
    fig.add_trace(
        go.Scatter(
            x=df["dateTime"],
            y=df["High Water Mark"],
            name="High Water",
            line=dict(color="#023f64", width=1, dash="dashdot"),
        )
    )

    # Add natural rim trace
    fig.add_trace(
        go.Scatter(
            x=df["dateTime"],
            y=df["Low Water Mark"],
            name="Natural Rim",
            line=dict(color="#023f64", width=1, dash="dot"),
        )
    )

    # Update layout of the plot
    fig.update_layout(
        margin=dict(t=20),
        title="Lake Tahoe Water Level",
        yaxis=dict(title=y_title),
        xaxis=dict(title=x_title, showgrid=False),
        hovermode=hovermode,
        template="plotly_white",
        dragmode=False,
        legend=dict(
            orientation="h",
            entrywidth=100,
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
        ),
    )

    # Update traces
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_yaxes(tickformat=format)
    fig.update_xaxes(
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=tickangle,
    )

    # Write figure to HTML
    fig.write_html(
        config={"displayModeBar": False},
        file=str(path_html),  # Convert Path object to string
        div_id=div_id,
    )

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'