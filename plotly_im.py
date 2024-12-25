import pandas as pd
import plotly.express as px

def plot_to_html(df: pd.DataFrame, x: str, y: str, labels: dict, color_based_on: str, y_label: str = "", x_label: str = "", title: str = "", filepath: str = "plot") -> str:
    # Create a bar plot with a greyscale color theme
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        labels=labels,
        color=color_based_on,
        color_continuous_scale=px.colors.sequential.Jet
    )

    # Update layout for appearance
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,  # Adding the y_label explicitly
        template="plotly_white",  # Light background for greyscale contrast
        title_x=0.5,  # Center the title
    )

    fig.write_image(f"{filepath}.png")
    return f"{filepath}.png"

def plot_pie_chart(df: pd.DataFrame, names: str, values: str, labels: dict, title: str = "", filepath: str = "plot") -> str:
    # Create a pie chart
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        labels=labels,
        color_discrete_sequence=px.colors.sequential.Jet
    )

    # Update layout for appearance
    fig.update_layout(
        template="plotly_white",  # Light background for greyscale contrast
        title_x=0.5  # Center the title
    )

    fig.write_image(f"{filepath}.png")
    return f"{filepath}.png"