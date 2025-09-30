import plotly.express as px
import plotly.data as pldata

# Load sample dataset
df = pldata.iris(return_type='pandas')  # returns a Pandas DataFrame

# Create an interactive scatter plot
fig = px.scatter(
    df,
    x='sepal_length',
    y='petal_length',
    color='species',
    title="Iris Data, Sepal vs. Petal Length",
    hover_data=["petal_length"]
)

# Save to HTML and open in browser
fig.write_html("iris.html", auto_open=True)
