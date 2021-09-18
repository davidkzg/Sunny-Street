import dash
from dash_bootstrap_components._components.Card import Card
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input,State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.SUPERHERO],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

viz = dbc.Card(
    [
        dbc.CardLink([
            dbc.CardImg(src="static/VSFG Logo to include on viz - dark background.png", className="card-img",style={"height" :"100%","width" : "100%"}),
        ], href="https://www.vizforsocialgood.com/",style={"height" :"100%","width" : "100%"}),
    ],
    style={"bottom" : "0","right":"0","position":"fixed","height" :"10%","width" : "40%"},
)

button_group = html.Div([
    html.H3("Pick a year for sentiment score of journal entry",className="ml-2"),
    dbc.ButtonGroup([dbc.Button("2019", id="btn1"), dbc.Button("2020",id="btn2"), dbc.Button("2021",id="btn3")]),
],)

simple_jumbotron = dbc.Jumbotron(
    [
        html.H1("Sunny Street", className="display-3"),
        html.P("Make sure that the Sunny Street volunteer stays happy and motivated!",className="lead",),
        html.P("Each entry in the journal entry has been given a score from -1 to 1, where -1 indicates a bad sentiment and 1 a happy sentiment. The 2 graphs show the sum of the sentiment in the given month",className="lead"),
    ],className="shadow-md rounded",style={"background-color": "#ED0C6E"},
)

df = pd.read_csv("sent_Journal.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.groupby(pd.Grouper(key='Date',freq='M')).sum()
fig = px.line(df, x=df.index, y="sent", title='Sentiment analysis through the years')
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=months,
    y=[0, 0, 0, 0, 0, 0, 0, 0.7, 4, 7.2, 3.4, 2.9],
    name='2019',
    marker_color='indianred'
))
fig1.add_trace(go.Bar(
    x=months,
    y=[4.8, 5.9, 2.3, 2.4, 8.3, 3.0, 5.1, 4.9, 10.6, 10, 12.7, 5],
    name='2020',
    marker_color='salmon'
))
fig1.add_trace(go.Bar(
    x=months,
    y=[0.8, 8.3, 7.1, 3.0, 0, 0, 0, 0, 0, 0, 0, 0],
    name='2021',
    marker_color='green'
))
fig1.update_layout(barmode='group', xaxis_tickangle=-45,title="Sentiment analysis over the years")

card = dbc.Card(
    [
        dcc.Graph(figure=fig),
    ],
)

card1 = dbc.Card(
    [
        dcc.Graph(figure=fig1),
    ],
)

card2 = dbc.Card([
    button_group,
])


card3 = html.Div([
    dbc.Row([
        dbc.Col([],xl=6,xs=12,id="Output1"),
        dbc.Col([],xl=6,xs=12,id="Output2"),],className="mt-2"),
])

data =  html.Div([
    dbc.Row([
        dbc.Col([simple_jumbotron],width=12,),
    ]),
    dbc.Row([
        dbc.Col([card],xl=6,xs=12),
        dbc.Col([card1],xl=6,xs=12),
    ]),
    dbc.Row([
        dbc.Col([card2],xs=12,lg=12),
    ],className="mt-2"),
    card3,
])


app.layout = html.Div(
    [
        dbc.Container([
                dcc.Location(id="url"),
                html.Div(id="page-content",children=[data],),
                viz,
            ],
            fluid=False),
    ],
    style={"height": "100vh"}
)

@app.callback(Output('Output1', 'children'),Output('Output2', 'children'),
              Input('btn1', 'n_clicks'),
              Input('btn2', 'n_clicks'),
              Input('btn3', 'n_clicks'))
def displayClick(btn1, btn2, btn3):
    df = pd.read_csv("sent_Journal.csv",index_col=0)
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1.n_clicks' == changed_id:
        df = df[df["Year"] == 2019]
        df = df.sort_values('sent')
        sus = df[df["sent"] > 0.0]
        sus = sus.sort_values('sent',ascending=False)
        neg = df[df["sent"] <= 0]
        neg = neg.sort_values('sent')
        successful = dbc.Table.from_dataframe(sus, striped=True, bordered=True, hover=True,style={"background-color":"#04AA6D"})
        dangerous = dbc.Table.from_dataframe(neg, striped=True, bordered=True, hover=True,style={"background-color":"red"})
        return successful,dangerous
    elif 'btn2.n_clicks' == changed_id:
        df = df[df["Year"] == 2020]
        df = df.sort_values('sent')
        sus = df[df["sent"] > 0.0]
        sus = sus.sort_values('sent',ascending=False)
        neg = df[df["sent"] <= 0]
        neg = neg.sort_values('sent')
        successful = dbc.Table.from_dataframe(sus, striped=True, bordered=True, hover=True,style={"background-color":"#04AA6D"})
        dangerous = dbc.Table.from_dataframe(neg, striped=True, bordered=True, hover=True,style={"background-color":"red"})
        return successful,dangerous        
    elif 'btn3.n_clicks' == changed_id:
        df = df[df["Year"] == 2021]
        df = df.sort_values('sent')
        sus = df[df["sent"] > 0.0]
        sus = sus.sort_values('sent',ascending=False)
        neg = df[df["sent"] <= 0]
        neg = neg.sort_values('sent')
        successful = dbc.Table.from_dataframe(sus, striped=True, bordered=True, hover=True,style={"background-color":"#04AA6D"})
        dangerous = dbc.Table.from_dataframe(neg, striped=True, bordered=True, hover=True,style={"background-color":"red"})
        return successful,dangerous
    else: return [""],[""]

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)