# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("D:\personal resources\coursera\lesson10_applied_science_capstone\csv file\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


sitename=spacex_df["Launch Site"].unique().tolist()

options_dropdown=[{"label" : "All Sites", "value": "ALL"}]

for item in sitename: 

    options_dropdown.append({'label': item, 'value': item})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div([
                        
                                        html.Label("Select Site"),
                                        dcc.Dropdown(
                                            id="site-dropdown",
                                            options=options_dropdown,
                                            value="ALL",
                                            placeholder="Place a holder here",
                                            searchable=True

                                        )
                                ]),

                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                    html.Div([
                        
                                        html.Label("Choose payload range"),
                                        dcc.RangeSlider(
                                            id="slider_id",
                                            min=0,max=10000,step=1000,
                                            marks={i: str(i) for i in range(0,10001,2500)},
                                            value=[2500,5000]

                                        )
                                ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def update_pie_figure(site_value): 

    site_filtered_first=spacex_df[["Launch Site","class"]]

    site_filtered_all=spacex_df.groupby("Launch Site")["class"].sum()

    site_filtered_all=pd.DataFrame(site_filtered_all.reset_index())

    if site_value=="ALL": 

        fig=px.pie(site_filtered_all,values="class",names="Launch Site",title="Total Success Launcher by Site")

        return fig 
    
    else: 

        site_filtered_singular=site_filtered_first[site_filtered_first["Launch Site"]==site_value]
        pie_df=site_filtered_singular.value_counts().reset_index()

        fig=px.pie(pie_df,values="count",names="class",title=f"Total Success launches by {site_value} ")

        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
     Input(component_id='slider_id',component_property='value')]
     
     )

def update_scatter_plot(site_id, silder_value): 

    min_value=silder_value[0]
    max_value=silder_value[1]

    payload_filtered=spacex_df[ (spacex_df["Payload Mass (kg)"]>min_value)  &  (spacex_df["Payload Mass (kg)"] < max_value) ]

    if site_id=="ALL":
        
        fig=px.scatter(payload_filtered, x="Payload Mass (kg)", y="class",color="Booster Version Category",
                   title='All launch site success rate over payload mass')
        
        return fig

    else: 

        fig=payload_filtered=payload_filtered[payload_filtered["Launch Site"]==site_id]

        px.scatter(payload_filtered, x="Payload Mass (kg)", y="class",color="Booster Version Category",
                   title=f'Launch site {site_id} success rate over payload mass')

        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()