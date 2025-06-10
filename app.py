from dash import Dash, dash_table, dcc, html, callback, Output, Input, State, MATCH
import dash_mantine_components as dmc

#data visualisation
import pandas as pd
import numpy as np
import glob

#graph
import plotly.express as px
import plotly.graph_objects as go


TWEETS_DATA_PATH = 'datasets/tweets'
CHAIN_DATA_PATH = 'datasets/network/network_data'
COIN_PRICE_PATH = 'datasets/network/prices'

tweet_df = pd.read_csv(f'{TWEETS_DATA_PATH}/tweets_all2.csv')
chain_df = pd.read_csv(f'{CHAIN_DATA_PATH}/bit_avg_all.csv')

if 'Unnamed: 0' in chain_df.columns:
    chain_df.drop(columns=['Unnamed: 0'], inplace=True)

app = Dash()

#variables for filter
unique_usernames = tweet_df.user_name.unique()
unique_usernames = np.append(unique_usernames, 'all')

'''
networks =['all', 'eth', 'poly', 'avax', 'bsc', 'arb','opt', 'ftm', 'base', \
                      'cro', 'aurora', 'celo', 'movr', 'linea', 'blast', 'mantle', \
                      'one', 'fuse', 'sepolia', 'pulse']
'''

networks = { "Bitcoin" : 'bit', "Doge": 'doge', "Ethereum": 'eth', \
            "Polygon": 'polygon', "Solana" : 'solana', "Optimism" : "optimisim", \
            "Tron" : 'tron', "fanthom" : 'fanthom', "Cronos" : "cronos",
            "Avalanche" : "avalanche", "Arbitrum" : "arbitrum", 'Binance' : 'binance'
            }

#declare available data for each network
avail_cat = {
    "Bitcoin" : ['Coin Price', 'txFee', 'txCount'] , "Doge": ['Coin Price', 'txCount', 'txFee'], \
    "Ethereum": ['Coin Price', 'gasPrice', 'txCount'], "Polygon": ['Coin Price', 'gasPrice', 'txCount'], \
    "Solana" : ['txFee', 'txCount'], "Optimism" : ['Coin Price', 'gasPrice'], \
    "Tron" : ['Coin Price', 'gasPrice'], "fanthom" :  ['Coin Price', 'gasPrice'], "Cronos" :  ['Coin Price', 'gasPrice'],
    "Avalanche" :  ['Coin Price', 'gasPrice'], "Arbitrum" :  ['Coin Price', 'gasPrice'], 'Binance': ['Coin Price']
}

chain_prices_cat = {'Coin Price' : "", 'txFee': "avg", 'gasPrice' : "gas", "txCount": "transac"}


selected_columns = { 'avg' : ['avg_fee', 'avg_value'], 'gas' : ['avg_gas_price_in_wei', 'avg_value_in_wei'], \
                     'transac' : ['avg_count']}

drop_columns = {'avg' : ['date'], 'gas' : ['date'], 'transac' : ['date']}

changing_df = tweet_df
#webapp layout
app.layout = html.Div(
    [
        html.H4(['Analysing tweets and blockchain data']),

        html.Div(className='row', children=[
            #filter username
            html.Label("Select an influencer twitter's User_name:"),
            html.Div(className='four columns', children=[
                dcc.Dropdown(
                    options = [ { 'label': x, 'value': x } for  x in unique_usernames ],
                    id='user-selected',
                    value='all'
                ),
            ], style={'width' : '10%', 'margin': '1%'})
        ]),

        #display original tweet data
        html.Div(className='row', id='tweet-df', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='graph-user')
            ])
        ]),

        #filter network
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                html.Label("Select an Network:"),
                dcc.Dropdown(
                    id="networkSelected",
                    value="Bitcoin",
                    options = [ { 'label': x, 'value': x } for  x in list(networks.keys()) ],
                ),
                html.Label("Select an Category:"),
                dcc.RadioItems(
                    options = list(chain_prices_cat.keys()),
                    id='priceCatSelected',
                    value='Coin Price',
                    inline=True,
                ),
            ]),
        ]),
        #show original blockchain data
        html.Div(className='row', id='blockchain-info', children=[
            html.Div(className='four columns', children=[
                dash_table.DataTable(data=chain_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
            ]),
            dcc.RadioItems(
                options=["Show Tweets Date", "Hide Tweets Date"],
                id='show-tweets',
                value="Show Tweets Date",
                inline=True,
            ),
        ]),
    ], style={'textAlign': 'center', 'color': 'black', 'fontSize': 12, 'background': 'white', 'margin': 10}
)

def get_curr_df(user, curr_df):
    '''
    Helper function to filter user tweets data
    '''
    if (user != 'all'):
        curr_df = tweet_df[tweet_df.user_name == user].copy()

    if ('Unnamed: 0' in curr_df.columns):
        curr_df.drop(columns=['Unnamed: 0'], inplace=True)
    return curr_df

def add_tweet_lines(fig, dates, y_max):
    '''
    Helper function to show when tweets were made
    '''
    for date in dates:
        fig.add_shape(
            type="line", x0=date, x1=date, y0=0, y1=y_max,
            line=dict(color="red", width=1, dash="dash")
        )
    return fig

@callback(
    Output(component_id='tweet-df', component_property='children'),
    Input(component_id='user-selected', component_property='value'),

)

def update_tweet_df(user):
    curr_df = get_curr_df(user, tweet_df)

    fig = go.Figure()
    analysis_output = curr_df.user_name.value_counts()
    fig = go.Figure(data=[
        go.Bar(x=analysis_output.index, y=analysis_output.values)
    ])

    main_output= curr_df.to_dict('records')
    return html.Div(className='four columns center', children=[
            html.H3("Tweets table"),
            dash_table.DataTable(data=main_output, id='tweet-df-output', page_size=12, style_table={'overflowX': 'auto'}),
            html.H3(f"This table consist of {curr_df.shape[0]} rows and {curr_df.shape[1]} columns"),
            dcc.Graph(figure=fig, id='tweet-df-analysis'),
        ]
    ),

@callback(
    Output(component_id='priceCatSelected', component_property='options'),
    Input(component_id='networkSelected', component_property='value'),
)

def update_cat(network) :
    return avail_cat[network]

@callback(
    Output(component_id='blockchain-info', component_property='children'),
    Input(component_id='networkSelected', component_property='value'),
    Input(component_id='priceCatSelected', component_property='value'),
    Input(component_id='user-selected', component_property='value'),
    Input(component_id='show-tweets', component_property='value')

)

def update_table(networkSelected, priceCatSelected, user, show_tweets):
    '''
    Purpose: retrieve network chain respective data and plot
    Input: blockchain network selected from dmc.SegmentedControl
    output :
        Graph objects
        -> candle graph of filtered networks and price cateogry type
    '''
    if priceCatSelected not in avail_cat[networkSelected]:
        priceCatSelected = chain_prices_cat[avail_cat[networkSelected][0]]
    else :
        priceCatSelected = chain_prices_cat[priceCatSelected]
    #print("INNNNNNNN")
    df = pd.read_csv('datasets/network/allnetworks.csv')
    #print(tweet_df)
    tweets_df = get_curr_df(user, tweet_df)
    print(tweet_df)
    if 'date' in tweets_df.columns:
        #tweets_df['date'] = pd.to_datetime(tweets_df['date'].map(lambda x : x[:19])).dt.date
        tweet_dates = pd.to_datetime(tweets_df['date'].map(lambda x : x[:10]).str.replace("/", "-", regex=False)).unique()
        tweet_dates = tweet_dates[tweet_dates > pd.to_datetime('2019-12-31')]
        #tweet_dates = tweet_dates[tweet_dates < pd.to_datetime('2025-01-01')]
        n = 20
        if (len(tweet_dates) < 20):
            n = len(tweet_dates)
        tweet_dates = pd.Series(tweet_dates).sample(n=n, random_state=42)

    #print(tweet_dates)
    if (priceCatSelected != '' and priceCatSelected != 'all'):
        df = pd.read_csv(f'{CHAIN_DATA_PATH}/{networks[networkSelected]}_{priceCatSelected}_all.csv')
    elif (priceCatSelected == ''):
        file = glob.glob(f"{COIN_PRICE_PATH}/{networks[networkSelected]}*")[0]
        df = pd.read_csv(file)

    if ('Unnamed: 0' in df.columns):
        df.drop(columns=['Unnamed: 0'], inplace=True)

    fig = go.Figure()
    #print(priceCatSelected)
    if (priceCatSelected == '') :
        df['Start'] = pd.to_datetime(df['Start'])
        fig.add_traces(go.Candlestick(x=df['Start'],
            open=df[f'Open'],
            high=df[f'High'],
            low=df[f'Low'],
            close=df[f'Close']))
        fig.update_layout(
            title=f"Coin Prices over time",
        )
        #print(df.Start.dtype)
        #print(df[f'Open'].astype(float).max())

        if show_tweets == 'Show Tweets Date':
           add_tweet_lines(fig, tweet_dates, df[f'Open'].astype(float).max())
        '''
        for date in tweet_dates:
            #print(date)
            fig.add_shape(
                type="line", x0=date, x1=date, y0=0, y1=df[f'Open'].astype(float).max(),
                line=dict(color="red", width=1, dash="dash")
            )
        '''



          #add_tweet_lines(fig, tweet_dates, df[f'Open'].astype(float).max())
        print("done")
        return html.Div(className='four columns center', children=[
            html.H3(f"{networkSelected} data table"),
            dash_table.DataTable(data=df.to_dict('records'), id='block-df-output', page_size=12, style_table={'overflowX': 'auto'}),
            html.H3(f"This table consist of {df.shape[0]} rows and {df.shape[1]} columns"),
            dcc.RadioItems(
                options=["Show Tweets Date", "Hide Tweets Date"],
                id='show-tweets',
                value=show_tweets,
                inline=True,
            ),
            dcc.Graph(figure=fig, id='block-df-analysis'),
        ]
    ),

    else :
        cols = selected_columns[priceCatSelected]
        all_figs = [] #concantenate the figures
        #print(cols)
        df['date'] = pd.to_datetime(df['date'])
        for col in cols:
            fig = go.Figure()
            fig.add_traces(
                go.Scatter(
                    x=df.date,
                    y=df[f'{col}'],
                    mode='lines+markers', name=f'{col}'
                )
            )
            print(df.date.dtype)

            if show_tweets == 'Show Tweets Date':
               add_tweet_lines(fig, tweet_dates, df[f'{col}'].max())
            '''
            if show_tweets == 'Show Tweets Date':
                for date in tweet_dates:
                    fig.add_shape(
                        type="line", x0=date, x1=date, y0=0, y1=df[f'{col}'].max(),
                        line=dict(color="red", width=1, dash="dash")
                    )
            '''

            fig.update_layout(
                title=f"{col} over time",
            )
            if len(cols) > 1:
                fig.update_layout(
                    xaxis_title="Date (drag to chose specific time frame)",
                    width=600,  # Set the width of the figure
                    height=600  # Set the height of the figure
                )

            all_figs.append(fig)
            # Example of changing figure size in the layout

        return html.Div(
            className='four columns center',
            children=[
                html.Label("Select a Network:"),
                html.H3(f" {networkSelected} Data Table"),
                dash_table.DataTable(data=df.to_dict('records'), id='block-df-output', page_size=12, style_table={'overflowX': 'auto'}),
                html.H3(f"This table consists of {df.shape[0]} rows and {df.shape[1]} columns"),
                dcc.RadioItems(
                    options=["Show Tweets Date", "Hide Tweets Date"],
                    id='show-tweets',
                    value=show_tweets,
                    inline=True,
                ),
                html.Div(
                    children=[
                        dcc.Graph(figure=fig, id=f'block-df-analysis-{i}')
                        for i, fig in enumerate(all_figs)
                    ],
                    style={
                        'display': 'flex' if len(all_figs) > 1 else 'block',
                    }
                ),
            ]
        )





if __name__ == '__main__':
    app.run(debug=True)