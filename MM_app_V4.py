import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

#City information for dropdown
CITY_DATA = 'dropdown_cities.csv'
city_df = pd.read_csv(CITY_DATA, header=None)
city_df.columns = ['City']


# Get Data and setup app with stylesheets
dfall = pd.read_csv('finaldata.csv')
dfall['text'] = dfall['Source airport'] + ' ' + dfall['Destination airport']
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

#Gather Info from User
card = dbc.Card(
    [
        dbc.Col(html.H5(children = "Enter Information")),
        dcc.Dropdown(
            options=[
                {"label": col, "value": col} for col in city_df['City']
            ],
            disabled=False,
        ),

        dbc.FormGroup(
            [
                dbc.Label("Enter Start City Number:"),
                dcc.Input(id="input1", placeholder='From', type = "number", min=0, max= 450, step=1)
            ],
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Enter Destination City Number:"),
                dcc.Input(id="input2", placeholder='To', type = "number", min=0, max= 450, step=1)
            ],
        ),
        dbc.Button(id='buttonSearch', n_clicks=0, children='Search',color = "primary", className= "mr-3"),
        dbc.Button(id='buttonCancel', n_clicks=0, children='Cancel', color = "danger", className = "mr-3"),
    ],
    body=True,
)

#Output for User
results = dbc.Card(
    [
     dbc.Col(html.H5(children = "Results")),
     dbc.ListGroup(
         [
             #UPDATE THIS INFORMATION
             dbc.ListGroupItem("Route:", color="info")]
        )
    ],
    body=True,
)

#App Layout
app.layout = dbc.Container(
    [
        #Title
        dbc.Row(
            dbc.Col(
                html.H2(children = "Kartemap: Finding the Shortest Airport Path")
            )
        ),    
        #Info from User & Map
        dbc.Row(
            [
                dbc.Col(card, width = 4),
                dbc.Col(dcc.Graph(id = 'map')),
            ],
            align = "center",
            ),
        #Results Section
        dbc.Row(
            [
                dbc.Col(results, width = 4)
            ],
            align = "center",
            ),
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)


#Backend Coding Stuff
import M3_new
def get_route1(fro, to): #cities
    start_end_path=M3_new.main(fro, to) #list of city names - start to end
    lons = []
    lats = []
    print(start_end_path)
    for c in start_end_path: #get lon and lat of each city in shortest path
        print(c)
        #print(dfall['Origin_city'])
        cityrow=dfall[dfall['Source_City'] == c]
        #print("**")
        #print(cityrow)
        if len(cityrow)==0:
            print("city name does not exist!")
            return 0, 0, 0
        cityrow=cityrow[:1]
        lons.extend(cityrow["Source_Longitude"]) #find city in original file
        lats.extend(cityrow["Source_Latitude"])
    return start_end_path, lats, lons # return a list of long/lat of destinations in shortest path

@app.callback(
    Output("map", "figure"),
    [Input("input1", "value"), 
     Input("input2", "value"), 
     Input('buttonSearch', 'n_clicks'), 
     Input('buttonCancel', 'n_clicks')]
)
def route_line(input1, input2, n_clicks1, n_clicks2):
    if (n_clicks1!=0):
        path, lats, lons = get_route1(input1, input2)
        if path==0:
            return "city name does not exist!"
        print(path)
        print(lats)
        print(lons)
        
        figure = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = [lons],
        lat = [lats],
        marker = {'size': 10}))        

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'accesstoken' : token,
                'style': "outdoors",
                'center': {'lon': -94, 'lat': 39},
                'zoom': 3})
        
        return figure

#Map Stuff
token = "pk.eyJ1IjoiMTJtbWFub2hhciIsImEiOiJja2hqeHBlNzgwM21wMnhwOHN4djh2ZHV3In0.dMIOKQThQPqnxpUVLmLgPw" 
fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [],
    lat = [],
    marker = {'size': 10}))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'accesstoken' : token,
        'style': "outdoors",
        #Use coordinates for Kansas AKA the middle of the US
        'center': {'lon': -94, 'lat': 39},
        'zoom': 3})

# Main
if __name__ == "__main__":
    app.run_server(debug= True)
