import dash
#import dash_core_components as dcc
from dash import dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df1 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

df2 = pd.read_csv('airbnb.csv')

df3 = pd.DataFrame({
  "Indicator": ["Total Cases", "Recovered", "Total Cases", "Recovered"],
  "Cases": [19111326, 11219123, 10147468, 9717834],
  "Country": ["USA", "USA", "India", "India"]
})

df_bank = pd.read_csv('https://raw.githubusercontent.com/rafiag/DTI2020/main/data/bank.csv')

def clean_data(df):
    
    # replacing numbers with strings
    df.neighborhood = df.neighborhood.map({1 : 'Friedrichshain-Kreuzberg', 2 : 'Mitte', 3 : 'Pankow', 4 : 'Neukölln', 5 :'Charlottenburg-Wilm',
                        6 : 'Tempelhof - Schöneberg', 7 : 'Lichtenberg', 8 : 'Treptow - Köpenick', 9 : 'Steglitz - Zehlendorf',
                        10 : 'Reinickendorf', 11 : 'Marzahn - Hellersdorf', 12 : 'Spandau'})

    df.room_type = df.room_type.map({1 : 'Entire home/apt', 2 : 'Private room', 3 : 'Shared room'})

    yes_no_dict = {0: 'No', 1:'Yes'}
    df.wifi = df.wifi.map(yes_no_dict)
    df.washer = df.washer.map(yes_no_dict)
    df.cable_tv = df.cable_tv.map(yes_no_dict)
    df.kitchen = df.kitchen.map(yes_no_dict)
    
    # renaming columns
    df.rename(columns={'neighborhood': 'Neighborhood', 'room_type': 'Room Type', 'accommodates': 'Accommodates',
                      'bedrooms': 'Bedrooms', 'number_of_reviews': 'Number of Reviews', 'wifi': 'Wifi', 'cable_tv': 'Cable TV',
                      'washer': 'Washer', 'kitchen': 'Kitchen', 'price': 'Price (US Dollars)'}, inplace=True)
    
    # removing outliers
    df = df[df['Price (US Dollars)']<501]
    
    return df

df2 = clean_data(df2)

df3 = pd.DataFrame({
  "Indicator": ["Total Cases", "Recovered", "Total Cases", "Recovered"],
  "Cases": [19111326, 11219123, 10147468, 9717834],
  "Country": ["USA", "USA", "India", "India"]
})

fig = px.bar(df, y="Fruit", x="Amount", color="City", barmode="group")

fig1 = px.scatter(df1, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)
fig1.update_layout(title='Life expectancy across continents')
                 
                 
                 
fig2 = px.scatter(df2, x='Neighborhood', y='Price (US Dollars)'
                 ,size='Accommodates'
                 , hover_data=['Bedrooms', 'Wifi', 'Cable TV', 'Kitchen', 'Washer', 'Number of Reviews']
                 ,color= 'Room Type')
fig2.update_layout(template='plotly_white')
fig2.update_layout(title='How much should you charge in a Berlin neighborhood?')

fig3 = px.bar(df3, x="Indicator", y="Cases", color="Country", barmode="group")
fig3.update_layout(title='Total cases vs recovered in the USA and India')

fig4 = px.scatter(df_bank, x = "age", y = "balance", color = "job",
  log_x = True, size_max = 60)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='Interactive App', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        Created this app as part of the assignment which holds atleast five charts.
    ''', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig1
    ),
    dcc.Graph(
        id='berlin',
        figure=fig2
    ),
    dcc.Graph(
        id='covidrecoveries',
        figure=fig3
    ),
    dcc.Graph(
        id='bubble',
        figure=fig4
    )    
])

if __name__ == '__main__':
    app.run_server(debug=True)
