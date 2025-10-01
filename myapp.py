from dash import Dash, dcc, html, Input, Output
import plotly.express as px                    
import pandas as pd

#use Plotly's built-in Gapminder dataset
gap = px.data.gapminder().sort_values(["country", "year"])

#unique countries for dropdown
countries = gap["country"].drop_duplicates().sort_values()

#initialize Dash app
app = Dash(__name__)
server = app.server # <-- This is the line you need to add

#layout - dropdown + graph
app.layout = html.Div([
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in countries],
        value="Canada",          #initial value per instructions
        clearable=False
    ),
    dcc.Graph(id="gdp-growth")
])

#callback, update figure when dropdown changes
@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(country_name):
    #filter rows for the selected country
    sub = gap[gap["country"] == country_name]
    fig = px.line(
        sub,
        x="year",
        y="gdpPercap",
        markers=True,
        title=f"GDP per Capita Over Time — {country_name}",
        labels={"year": "Year", "gdpPercap": "GDP per Capita (USD)"}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig

#run app
if __name__ == "__main__":
    app.run(debug=True)   #visit http://localhost:8050
