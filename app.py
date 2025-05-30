from dash import Dash, dash_table, dcc, callback, Output, Input
import dash_mantine_components as dmc

#data
import pandas as pd

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
unique_usernames.append('all')
networks =['all', 'eth', 'poly', 'avax', 'bsc', 'arb','opt', 'ftm', 'base', \
                      'cro', 'aurora', 'celo', 'movr', 'linea', 'blast', 'mantle', \
                      'one', 'fuse', 'sepolia', 'pulse']

#webapp layout
app.layout = dmc.Container([
    dmc.Title('Analysing tweets and blockchain data', color="blue", size="h3"),

    #filter username
    dmc.RadioGroup(
            [dmc.Radio(i, value=i) for i in  unique_usernames],
            id='user-selected',
            value='usernames',
            size="sm"
        ),

    #display original tweet data
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(data=tweet_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], span=6),
        dmc.Col([
            dcc.Graph(figure={}, id='graph-user')
        ], span=6),
    ]),

    #filter network
    dmc.SegmentedControl(
            id="segmented",
            value="all",
            data= networks,
            mb=10,
        ),
    #show original blockchain data
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(data=chain_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], span=6),
        dmc.Col([
            dcc.Graph(figure={}, id='block-graph')
        ], span=6),
    ]),

], fluid=True)

@callback(
    Output(component_id='graph-user', component_property='figure'),
    Input(component_id='user-selected', component_property='value'),

    Output(component_id='block-graph', component_property='figure'),
    Input(component_id='networkSelected', component_property='value')
)
def update_graph(networkSelected):
    if (networkSelected != 'all'):
        df = pd.read_csv(f'{CHAIN_DATA_PATH}/{networkSelected}_all.csv')
    else :
        df = pd.read_csv(f'{CHAIN_DATA_PATH}/allnetworks.csv')




    return fig

if __name__ == '__main__':
    app.run(debug=True)