import plotly.express as px
import pandas as pd
from config import MONTH_NAMES, CITY_COLORS


def plot_monthly_sunshine(df_monthly_data: pd.DataFrame) -> object:
    """ Creates a clear bar chart showing the monthly average daily sunshine duration for each city.

    Parameters: DataFrame containing the following columns: 'month', 'city' and 'mean_sunshine_duration'.
    Returns: A Plotly Figure object containing the grouped bar chart, ready for rendering in Streamlit or Jupyter Notebook.
    """

    df_monthly_data["month_name"] = df_monthly_data["month"].map(MONTH_NAMES)

    fig = px.bar(df_monthly_data, 
                 x="month_name", 
                 y="mean_sunshine_duration", 
                 color="city", 
                 barmode="group",
                 color_discrete_map=CITY_COLORS,
                 title="Měsíční průměr denní délky slunečního svitu",
                 labels={"month_name": "Měsíc",
                         "mean_sunshine_duration": "Průměrná doba denního svitu (h)",
                         "city": "Město"}
                )
    fig.update_xaxes(
        categoryorder="array",
        categoryarray=list(MONTH_NAMES.values()),
        tickmode="array",  # vlastní interval pojmenování
        tickvals=list(MONTH_NAMES.values()),
        ticktext=list(MONTH_NAMES.values()),
        range=[-0.5, 11.5]  # odsazení od okrajů grafu
        )
    
    fig.update_yaxes(
        dtick=1,
        showgrid=True,
        gridwidth=0.5,
        gridcolor="lightgrey"
        )
    
    return fig