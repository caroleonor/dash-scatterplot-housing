import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'DC Housing'
myheading='Analysis of housing prices in Washington DC'
neighborhood='Georgetown'
color1='#04F9E6'
color2='#1B03B1'
sourceurl = 'https://www.kaggle.com/christophercorrea/dc-residential-properties/'
githublink = 'https://github.com/caroleonor/dash-scatterplot-housing/edit/master/app.py'

########### Prepare the dataframe 
#filter data before analysis, because it won't cluster
df = pd.read_csv('DC_Properties.csv') #if it's in the folder, just put the file name without path
df=df[df['ASSESSMENT_NBHD']==neighborhood] #assign df to df, [[]] means it's a filter
df=df[(df['PRICE']<=1000000) & (df['PRICE']>=10000)]
df=df[df['LANDAREA']<4000]
df=df[df['PRICE']<900000]
df=df[df['BEDRM']<8]

########### Set up the chart
trace = go.Scatter(
    x = df['PRICE'],
    y = df['LIVING_GBA'],
    mode = 'markers',
    marker=dict(
        size=8,
        color = df['BEDRM'], # set color equal to a third variable, this is the 3rd variable 
        colorscale=[color1, color2], #this is the continueity variable, default will be grey to black if don't set up color 
        colorbar=dict(title='Bedrooms'),
        showscale=True
    )
)

#trace and layout if the user can select the neighborhood 
data = [trace]
layout = go.Layout(
    title = f'Larger homes cost more in {neighborhood}!', # Graph title
    xaxis = dict(title = 'Sales Price'), # x-axis label
    yaxis = dict(title = 'Square Feet'), # y-axis label
    hovermode ='closest' # handles multiple points landing on the same vertical
)
fig = go.Figure(data=data, layout=layout)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='figure-1',
        figure=fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Deploy
if __name__ == '__main__':
    app.run_server()
