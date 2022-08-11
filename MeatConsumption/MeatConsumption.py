import pandas as pd
import folium
import geopandas
from flask import Flask

app = Flask(__name__)

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_meat_consumption'
tables = pd.read_html(url)
table = tables[1]

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

table = world.merge(table, how='left', left_on=['name'], right_on=['Country'])


my_map = folium.Map(location=[0, 0], zoom_start=2)
folium.Choropleth(
    geo_data=table,
    name="choropleth",
    data=table,
    columns=["Country", 'kg/person (2002)[9][note 1]'],
    key_on="feature.properties.name",
    fill_color="OrRd",
    fill_opacity=0.7,
    line_opacity=0.6,
    nan_fill_opacity=0.2,
    legend_name="Meat Consumption in kg/person (2002)",
).add_to(my_map)


@app.route('/')
def index():
    return my_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
