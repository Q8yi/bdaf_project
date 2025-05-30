from dash import Dash, dash_table, dcc, html, callback, Output, Input
import dash_mantine_components as dmc

#data
import pandas as pd
import numpy as np

#graph
import plotly.express as px
import plotly.graph_objects as go


TWEETS_DATA_PATH = 'data/tweets'
CHAIN_DATA_PATH = 'data/network'
tweet_df = pd.read_csv(f'{TWEETS_DATA_PATH}/tweet_final.csv')
chain_df = pd.read_csv(f'{CHAIN_DATA_PATH}/arb_all.csv')


app = Dash()

#variables for filter
unique_usernames = tweet_df.user_name.unique()
unique_usernames = np.append(unique_usernames, 'all')
networks =['all', 'eth', 'poly', 'avax', 'bsc', 'arb','opt', 'ftm', 'base', \
                      'cro', 'aurora', 'celo', 'movr', 'linea', 'blast', 'mantle', \
                      'one', 'fuse', 'sepolia', 'pulse']
chain_prices_cat = ['tokenPrice', 'txFee', 'gasPrice', 'all']
#webapp layout

app.layout = html.Div(
    [
        html.H4(['Analysing tweets and blockchain data']),

        html.Div(className='row', children=[
            #filter username
            html.Div(className='four columns', children=[
                dcc.Dropdown(
                    options = [ { 'label': x, 'value': x } for  x in unique_usernames ],
                    id='user-selected',
                    value='all'
                ),
            ], style={'width' : '10%', 'margin': '1%'})
        ]),

        #display original tweet data
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                    dash_table.DataTable(data=tweet_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
                ]
            ),
            html.Div(className='six columns', children=[
                    dcc.Graph(figure={}, id='graph-user')
            ]),
        ]),

        #filter network
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dcc.Dropdown(
                    id="networkSelected",
                    value="all",
                    options = [ { 'label': x, 'value': x } for  x in networks ],
                    ),
                ], style={'width' : '10%'}),

            html.Div(className='four columns', children=[
                dcc.RadioItems(
                    options = chain_prices_cat,
                    id='priceCatSelected',
                    value='tokenPrice',
                    inline=True,
                ),
            ]),
        ]),
        #show original blockchain data
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dash_table.DataTable(data=chain_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='block-graph')
            ]),
        ]),

    ], style={'textAlign': 'center', 'color': 'black', 'fontSize': 12, 'background': 'white', 'margin': 10}
)

@callback(
    Output(component_id='block-graph', component_property='figure'),
    Input(component_id='networkSelected', component_property='value'),
    Input(component_id='priceCatSelected', component_property='value'),

)
def update_graph(networkSelected, priceCatSelected):
    '''
    Purpose: retrieve network chain respective data and plot
    Input: blockchain network selected from dmc.SegmentedControl
    output :
        Graph objects
        -> candle graph of filtered networks and price cateogry type
    '''
    if (networkSelected != 'all'):
        df = pd.read_csv(f'{CHAIN_DATA_PATH}/{networkSelected}_all.csv')
    else :
        df = pd.read_csv(f'{CHAIN_DATA_PATH}/allnetworks.csv')

    fig = go.Figure()
    if (priceCatSelected != 'all') :
        fig.add_traces(go.Candlestick(x=df.timestamp,
                    open=df[f'{priceCatSelected}_open'],
                    high=df[f'{priceCatSelected}_high'],
                    low=df[f'{priceCatSelected}_low'],
                    close=df[f'{priceCatSelected}_close']))

    else :
        for price in chain_prices_cat[:3]:
            fig.add_traces(go.Candlestick(x=df.timestamp,
                    open=df[f'{price}_open'],
                    high=df[f'{price}_high'],
                    low=df[f'{price}_low'],
                    close=df[f'{price}_close']))

    fig.update_layout(xaxis_rangeslider_visible=False,
                    title = f'{networkSelected} prices over time',
                    xaxis_title="Date (drag to chose specific time frame)"
                    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)