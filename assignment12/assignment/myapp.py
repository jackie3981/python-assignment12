from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata

# load gapminder dataset
df = pldata.gapminder(return_type='pandas')

# Get list of unique countries
countries = df['country'].unique()

# Initialize Dash app
app = Dash(__name__)
# Task 5: Deploying to Render.com
server = app.server

# layout: dropdown + graph
app.layout = html.Div([
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": country, "value": country} for country in countries],
        value="Canada"  # initial value
    ),
    dcc.Graph(id="gdp-growth")
])

# Callback to update the graph based on selected country
@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(selected_country):
    # Filtrar filas por país
    filtered_df = df[df['country'] == selected_country]
    
    # Crear gráfico de línea: year vs gdpPercap
    fig = px.line(
        filtered_df,
        x="year",
        y="gdpPercap",
        title=f"GDP per Capita Growth for {selected_country}"
    )
    return fig

# Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True)
