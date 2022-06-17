'''

########
packages used :

dash : Dash is a python framework created by plotly for creating interactive web applications.
 Dash is written on the top of Flask, Plotly. js and React. js

plotly : The plotly Python library is an interactive, open-source plotting library that supports over 40 unique chart types
 covering a wide range of statistical, financial, geographic, scientific, and 3-dimensional use-cases

pandas : pandas is a Python package providing fast, flexible, and expressive data structures
 designed to make working with “relational” or “labeled” data both easy and intuitive.
 It aims to be the fundamental high-level building block for doing practical, real-world data analysis in Python.

dash-bootstrap-components : dash-bootstrap-components is a library of Bootstrap components for use with Plotly Dash,
 that makes it easier to build consistently styled Dash apps with complex, responsive layouts.

flask : used to handle server side operations of dash app as dash is written on the top of flask

base64 : used to encode and decode data like images

os : provides functions for interacting with the operating system

to install all packages with pip use this command :
pip install dash plotly dash-bootstrap-components flask pandas
######

######
Project files:

main.py : where the main dash app runs from and front end and server side code is written

charts.py : where a functions that generate different kind of charts is written that main.py file use and also some other text cleanining functions

twitter_dataset.csv : the file where all te=witter data used exist in

assets folder : its very important as all the .css files used for custom styling exists there and the folder must exist in project directory
in order to make these custom styles appears ( note that these styles are extra ones beside the main styles generate from python code in
the components style parameter )

logo.png: the logo image used in app

All Topics.png , Aviation.png , Cristiano ronaldo.png , Gun control.png , Housing.png , Military.png , Rehab.png :
all these are images produced by wordcloud library and used in app to be read directly instead of repeating wordcloud code every time
so that saves processing time


'''
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import pandas as pd
import base64
import plotly.graph_objects as go
from flask import Flask
import os
import charts

'''
making flask server instance to be used as argument in dash app instance
'''
server = Flask(__name__)
'''
making dash app instance to be used to link the layout and callbacks to it
and giving it some configerations arguments like the server instance and making app width fits the screen 
'''
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
        }
    ] ,
)

'''
giving a title to the app to be displayed in browser tab
'''
app.title='Twitter Sentiment Analysis'
'''
giving a flexibility to callback functions to exist even if the layout changes
'''
app.config.suppress_callback_exceptions = True




'''
getting our project folder directory
'''
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
'''
getting our logo image directory
'''
logo_file=os.path.join(THIS_FOLDER, 'logo.png')
'''
getting our csv file directory
'''
csv_file=os.path.join(THIS_FOLDER, 'twitter_dataset.csv')

'''
##### layout creation starts here
'''

'''
creating the app header text
'''
header_text=html.Div('Twitter Sentiment Analysis Dashboard',id='main_header_text',className='main-header',
                     style=dict(color='#1dabdd',
                     fontWeight='bold',width='100%',paddingTop='1vh',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

'''
styling the width of app header text in different screen sizes
'''
db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=7,offset=0), sm=dict(size=7,offset=0),
        md=dict(size=8,offset=0), lg=dict(size=8,offset=0), xl=dict(size=8,offset=0))

'''
encoding our app logo image and creating image component where the encoded image exists in
'''
encoded = base64.b64encode(open(logo_file, 'rb').read())
logo_img=html.Div( html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img',className='mylogo'

                  )
                   ,style=dict(paddingTop='2vh',paddingLeft='2vw',paddingBottom='0.5vh'))

'''
styling the width of app logo image in different screen sizes
'''
db_logo_img=dbc.Col([ logo_img] ,
        xs=dict(size=3,offset=0), sm=dict(size=3,offset=0),
        md=dict(size=2,offset=0), lg=dict(size=2,offset=0), xl=dict(size=2,offset=0))

'''
reading our csv file 
'''
df= pd.read_csv(csv_file)

'''
converting 'created' column type to datetime
'''
df["created"]= pd.to_datetime(df["created"],infer_datetime_format=True )

'''
converting 'sentiment' column type to string
'''
df['sentiment']=df['sentiment'].astype(str)

'''
cleaning text column using functions in charts.py file
'''
df['text']=df['text'].apply(lambda text :charts.clean_data(text) )
df['text']=df['text'].apply(lambda text :charts.remove_puncts(text) )
df['text']=df['text'].apply(lambda text :charts.remove_stop_words(text) )
df['text']=df['text'].apply(lambda text :charts.processed_tweet(text) )
df['text']=df['text'].apply(lambda text :charts.cleaning_numbers(text) )

'''
creating the header of number of tweets box
'''
tweets_num_text= html.Div(html.H1('Total Number of Tweets',className= 'info-header',id='tweets_num_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict( textAlign="center", width='100%'))

'''
getting total no. tweets from the dataframe
'''
tweets_num=df['tweetId'].count()

'''
creating an indicator figure and adding it to dash graph component to show total no. tweets
'''

tweets_num_fig = go.Figure()

indicator_size=27
tweets_num_fig.add_trace(go.Indicator(
    mode = "number",
    value = tweets_num,
    number={'font':{'color':'#1dabdd','size':indicator_size},'valueformat':","},
   domain={'row':0,'column':0}
))

tweets_num_fig.update_layout(paper_bgcolor = "#f7f7f7",plot_bgcolor='white',height=50,margin=dict(l=0, r=0, t=0, b=0),

                  )

tweets_num_indicator=html.Div(dcc.Graph(figure=tweets_num_fig,config={'displayModeBar': False},id='tweets_num_indicator',style=dict(width='100%')),className='num'
                           , style=dict(width='100%')  )


'''
creating the header of average no. retweets box
'''

retweets_avg_text= html.Div(html.H1('Average Number of Retweets',className= 'info-header',id='retweets_avg_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
getting average no. retweets from the dataframe
'''
retweets_avg=round(df['tweet_retweet_count'].mean() , 1)

'''
creating an indicator figure and adding it to dash graph component to show average no. retweets
'''

retweets_avg_fig = go.Figure()

retweets_avg_fig.add_trace(go.Indicator(
    mode = "number",
    value = retweets_avg,
    number={'font':{'color':'#1dabdd','size':indicator_size},'suffix':"%"},
   domain={'row':0,'column':0}
))

retweets_avg_fig.update_layout(paper_bgcolor = "#f7f7f7",plot_bgcolor='white',height=50,margin=dict(l=0, r=0, t=0, b=0),

                  )

retweets_avg_indicator=html.Div(dcc.Graph(figure=retweets_avg_fig,config={'displayModeBar': False},id='retweets_avg_indicator',style=dict(width='100%')),className='num'
                           , style=dict(width='100%')  )

'''
creating the header of average no. likes box
'''
likes_avg_text= html.Div(html.H1('Average Number of Likes',className= 'info-header',id='likes_avg_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
getting average no. likes from the dataframe
'''

likes_avg=int(df['tweet_like_count'].mean() )

'''
creating an indicator figure and adding it to dash graph component to show average no. likes
'''
likes_avg_fig = go.Figure()

likes_avg_fig.add_trace(go.Indicator(
    mode = "number",
    value = likes_avg,
    number={'font':{'color':'#1dabdd','size':indicator_size},'suffix':"%"},
   domain={'row':0,'column':0}
))

likes_avg_fig.update_layout(paper_bgcolor = "#f7f7f7",plot_bgcolor='white',height=50,margin=dict(l=0, r=0, t=0, b=0),

                  )

likes_avg_indicator=html.Div(dcc.Graph(figure=likes_avg_fig,config={'displayModeBar': False},id='likes_avg_indicator',style=dict(width='100%')),className='num'
                           , style=dict(width='100%')  )

'''
creating the header of average no. replies box
'''
replies_avg_text= html.Div(html.H1('Average Number of Replies',className= 'info-header',id='replies_avg_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
getting average no. replies from the dataframe
'''
replies_avg=int(df['tweet_reply_count'].mean() )

'''
creating an indicator figure and adding it to dash graph component to show average no. replies
'''
replies_avg_fig = go.Figure()

replies_avg_fig.add_trace(go.Indicator(
    mode = "number",
    value = replies_avg,
    number={'font':{'color':'#1dabdd','size':indicator_size},'suffix':"%"},
   domain={'row':0,'column':0}
))

replies_avg_fig.update_layout(paper_bgcolor = "#f7f7f7",plot_bgcolor='white',height=50,margin=dict(l=0, r=0, t=0, b=0),

                  )

replies_avg_indicator=html.Div(dcc.Graph(figure=replies_avg_fig,config={'displayModeBar': False},id='replies_avg_indicator',style=dict(width='100%')),className='num'
                           , style=dict(width='100%')  )


'''
creating the header of total no. countries box
'''
countries_num_text= html.Div(html.H1('Total Number of Countries',className= 'info-header',id='countries_num_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))


'''
getting total no. countries from the dataframe
'''
countries_num=int(df['country'].nunique() )

'''
creating an indicator figure and adding it to dash graph component to show total no. countries
'''
countries_num_fig = go.Figure()

countries_num_fig.add_trace(go.Indicator(
    mode = "number",
    value = countries_num,
    number={'font':{'color':'#1dabdd','size':indicator_size},'valueformat':","},
   domain={'row':0,'column':0}
))

countries_num_fig.update_layout(paper_bgcolor = "#f7f7f7",plot_bgcolor='white',height=50,margin=dict(l=0, r=0, t=0, b=0),

                  )

countries_num_indicator=html.Div(dcc.Graph(figure=countries_num_fig,config={'displayModeBar': False},id='countries_num_indicator',style=dict(width='100%')),className='num'
                           , style=dict(width='100%')  )

'''
gettng a unique list of topics from dataframe
'''
topics=list(df['topic'].unique())

'''
inserting All Topics value in the list
'''
topics.insert(0,'All Topics')

'''
creating dash dropdown menu to select topic from it 
'''
topics_menu = dcc.Dropdown(className="custom-dropdown",
                            id='topics_menu',

                            options=[{'label': topic.capitalize(), 'value': topic} for topic in topics]
                            ,
                            value='All Topics',
                            style=dict(color='#1dabdd', fontWeight='bold', textAlign='center',
                                       width='16vh', backgroundColor='#1dabdd', border='1px solid black')
                            )

topics_text = html.Div(html.H1('Topics',
                                style=dict(fontSize='1.5vh', fontWeight='bold', color='black' )))

topics_menu_div = html.Div([topics_menu],
                            style=dict(fontSize='1.7vh',paddingTop='1vh',textAlign='center',display= 'flex',
                                       alignItems= 'center', justifyContent= 'center',width='100%'
                                       ))

topics_div=html.Div([topics_menu_div],style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                           'justify-content': 'center'})

'''
##### Number of Tweets Over Days by Topic


creating header of the line chart graph
'''
date_chart_header= html.Div(html.H1('Number of Tweets Over Days by Topic',className= 'date-chart-header',id='date_chart_header',
                                    style=dict( fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
creating the line chart graph component ( filled with empty figure in beginning to be updated from the callback
when app starts depending on topics dropdown menu value )
'''
date_chart=go.Figure(go.Scatter())
date_chart_div=html.Div([
            dcc.Graph(id='date_chart', config={'displayModeBar': True,'displaylogo': False,'modeBarButtonsToRemove': ['lasso2d','pan']},className='date-fig',
                style=dict(backgroundColor='#f7f7f7') ,figure=date_chart
            ) ] ,id='date_chart_div'
        )

'''
##### Sentiment Score by Topic


creating header of the horizontal bar chart graph
'''
hor_bar_chart_header= html.Div(html.H1('Sentiment Score by Topic',className= 'date-chart-header',id='hor_bar_chart_header',
                                    style=dict(fontWeight='bold', color='black',
                                               marginTop='')),
                            style=dict(textAlign="center", width='100%'))

'''
creating the horizontal bar chart graph component where we got the figure from charts.py function
'''
hor_bar_chart=charts.create_hor_bar(df)
hor_bar_chart_div=html.Div([
            dcc.Graph(id='hor_bar_chart', config={'displayModeBar': True,'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d','pan','zoom2d','zoomIn2d','zoomOut2d','autoScale2d']}
                      ,className='hor-bar-fig',
                style=dict(height='',backgroundColor='#f7f7f7',border='') ,figure=hor_bar_chart
            ) ] ,id='hor_bar_chart_div'
        )

'''
##### Top 5 Cities With Tweets


creating header of the vertical bar chart graph 
'''
ver_bar_chart_header= html.Div(html.H1('Top 5 Cities With Tweets',className= 'date-chart-header',id='ver_bar_chart_header',
                                    style=dict( fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
creating a countries/cities radio button to choose from for the vertical bar chart
'''
location_filter = html.Div(
    [
        dbc.RadioItems( options=[ {"label": "Countries", "value": 'country'},
                                  {"label": "Cities", "value": 'city'},],
            value='city',
            id="location_filter",
            inline=True, label_class_name='filter-label',input_class_name='filter-button',input_checked_class_name='filter-button-checked' ,
            input_checked_style=dict(backgroundColor='#1dabdd',border='2px solid #1dabdd')
        ),
    ]
)

'''
creating the vertical bar chart graph component where we got the figure from charts.py function
( filled with empty figure in beginning to be updated from the callback
when app starts depending on countries/cities radio buttons selected )
'''
ver_bar_chart=go.Figure(go.Bar())
ver_bar_chart_div=html.Div([
            dcc.Graph(id='ver_bar_chart', config={'displayModeBar': True,'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d','pan','zoom2d','zoomIn2d','zoomOut2d','autoScale2d']}
                      ,className='ver-bar-fig',
                style=dict(backgroundColor='#f7f7f7') ,figure=ver_bar_chart
            ) ] ,id='ver_bar_chart_div'
        )

'''
##### wordcloud part

wordcloud images was originally created from this code :

    for ind in graph_data.index:
        text += graph_data['text'][ind]

    wordcloud = WordCloud(max_font_size=60, max_words=100, background_color="#f7f7f7",
  collocations=False,
                      random_state = 42,relative_scaling = 0.3,
                      colormap = 'turbo',
                      repeat = False,
                      normalize_plurals = True).generate(text)
    plt.figure(facecolor='#f7f7f7')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(wordcloud_dir, facecolor='#f7f7f7', bbox_inches='tight')
    
we used images saved from this code to directly read them into the app for better performance
'''

'''
getting word cloud image directory
'''
wordcloud_dir=os.path.join(THIS_FOLDER, 'All Topics.png')

'''
encoding wordcloud image
'''
encoded = base64.b64encode(open(wordcloud_dir, 'rb').read())

'''
image header
'''
word_cloud_header= html.Div(html.H1('Word Cloud by Topic',className= 'word-cloud-header',id='word_cloud_header',
                                    style=dict(fontWeight='bold', color='black',
                                               )),
                            style=dict(textAlign="center"))

'''
adding image to dash html image component
'''
word_cloud=html.Div( html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='word_cloud',className='word-cloud'

                  )
                    )

'''
making another topic menu same as before but this time will be used with wordcloud
'''
topics_menu2 = dcc.Dropdown(className="custom-dropdown",
                            id='topics_menu2',

                            options=[{'label': topic.capitalize(), 'value': topic} for topic in topics]
                            ,
                            value='All Topics',
                            style=dict(color='#1dabdd', fontWeight='bold', textAlign='center',
                                       width='16vh', backgroundColor='#1dabdd', border='1px solid black')
                            )


topics_menu_div2 = html.Div([topics_menu2],
                            style=dict(fontSize='1.7vh',paddingTop='0.5vh',textAlign='center',display= 'flex',
                                       alignItems= 'center', justifyContent= 'center',width='100%'
                                       ))


'''
##### Number of Tweets by Country Map


creating header of the map
'''


map_header= html.Div(html.H1('Number of Tweets by Country',className= 'date-chart-header',id='map_header',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))
'''
creating the map component where we got the figure from charts.py function
'''
map_fig=charts.create_countries_map(df)
map_div=html.Div([
            dcc.Graph(id='map_fig', config={'displayModeBar': True,'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d','pan']}
                      ,className='map-fig',
                style=dict(height='',backgroundColor='#f7f7f7',border='') ,figure=map_fig
            ) ] ,id='map_div'
        )


'''
creating a dataframe that will be used in donut chart to get percentages of reliability categories
'''

dff=df.groupby('Reliability Categories')['tweetId'].count()
dff=dff.reset_index()

'''
adjusting the order of the reliability categories will be shown on donut chart
'''

temp=dff.loc[0]
dff.loc[0]=dff.loc[4]
dff.loc[4]=temp
temp=dff.loc[1]
dff.loc[1]=dff.loc[4]
dff.loc[4]=temp
temp=dff.loc[2]
dff.loc[2]=dff.loc[3]
dff.loc[3]=temp
temp=dff.loc[1]
dff.loc[1]=dff.loc[2]
dff.loc[2]=temp


'''
##### Tweets Reliability Levels Donut Chart
'''

donut_header= html.Div(html.H1('Tweets Reliability Levels',className= 'date-chart-header',id='donut_header',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))

'''
creating the donut component 
'''
donut = go.Figure(data=go.Pie(labels=dff['Reliability Categories'], values=dff['tweetId'],hole=.3,showlegend=False,sort=False))
donut.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=14, textfont_family='Arial',
                  marker=dict(colors=['#009191','#3B98F5','#46FFFF','#1500FF','#A5ECFF'], line=dict(color='#0f2937')),
                    texttemplate = '<b>%{label}</br></br>%{percent}</b>')

donut.update_layout(
    font=dict(size=14, family='Arial', color='black')
    ,hoverlabel=dict(font_size=14, font_family="Rockwell")
    , plot_bgcolor='#f7f7f7',
    paper_bgcolor='#f7f7f7', margin=dict(l=0, r=0, t=20, b=0)

)


donut_div=html.Div([
            dcc.Graph(id='map_fig', config={'displayModeBar': False,'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d','pan']}
                      ,className='donut-fig',
                style=dict(backgroundColor='#f7f7f7') ,figure=donut
            ) ] ,id='donut_div'
        )


'''
adding all of the app components in app.layout object 
the design made using dash-bootstrap columns , rows and cards
'''
main_layout=html.Div([dbc.Row([db_logo_img,db_header_text],
                              style=dict(backgroundColor='white'),id='main_header' ),
                      #html.Br(),

                    dbc.Row([
                        html.Div([

                      dbc.Card(dbc.CardBody([tweets_num_text,
                                                      dbc.Spinner([tweets_num_indicator], size="lg", color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ])
                                        , style=dict(backgroundColor='#f7f7f7'), id='card3',
                                        className='info-card'),


                      dbc.Card(dbc.CardBody([retweets_avg_text,
                                                      dbc.Spinner([retweets_avg_indicator], size="lg", color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ])
                                        , style=dict(backgroundColor='#f7f7f7',marginLeft='1vw'), id='card4',
                                        className='info-card'),

                        dbc.Card(dbc.CardBody([likes_avg_text,
                                                        dbc.Spinner([likes_avg_indicator], size="lg",
                                                                    color="primary",
                                                                    type="border", fullscreen=False,
                                                                    spinner_style=dict(marginTop=''))

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7',marginLeft='1vw'), id='card4',
                                          className='info-card'),

                        dbc.Card(dbc.CardBody([replies_avg_text,
                                                        dbc.Spinner([replies_avg_indicator], size="lg",
                                                                    color="primary",
                                                                    type="border", fullscreen=False,
                                                                    spinner_style=dict(marginTop=''))

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7',marginLeft='1vw'), id='card5',
                                          className='info-card'),

                       dbc.Card(dbc.CardBody([countries_num_text,
                                                        dbc.Spinner([countries_num_indicator], size="lg",
                                                                    color="primary",
                                                                    type="border", fullscreen=False,
                                                                    spinner_style=dict(marginTop=''))

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7',marginLeft='1vw'), id='card6',
                                          className='info-card'),
                                           ],style=dict(display= 'flex', alignItems= 'center',
                                                        justifyContent= 'center',width='100%'))
                                            ]),
                        html.Br(),

                      dbc.Row([
                        dbc.Col([dbc.Card(dbc.CardBody([date_chart_header,
                                                        dbc.Spinner([date_chart_div], size="lg", color="primary", type="border",
                                                                    fullscreen=False) , topics_div

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7'), id='card7',
                                          className='charts-card'), html.Br()
                                 ], xl=dict(size=5, offset=0), lg=dict(size=6, offset=0),
                                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                style=dict(paddingLeft='0.5vw',paddingRight='0.5vw')),

                        dbc.Col([dbc.Card(dbc.CardBody([hor_bar_chart_header,
                                                        dbc.Spinner([hor_bar_chart_div], size="lg", color="primary",
                                                                    type="border",
                                                                    fullscreen=False),

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7'), id='card8',
                                          className='charts-card'), html.Br()
                                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                style=dict(paddingLeft='0.5vw',paddingRight='0.5vw')),

                        dbc.Col([dbc.Card(dbc.CardBody([ver_bar_chart_header,
                                                        dbc.Spinner([ver_bar_chart_div], size="lg", color="primary",
                                                                    type="border",
                                                                    fullscreen=False),location_filter

                                                        ])
                                          , style=dict(backgroundColor='#f7f7f7'), id='card9',
                                          className='charts-card'), html.Br()
                                 ], xl=dict(size=3, offset=0), lg=dict(size=4, offset=0),
                                md=dict(size=4, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                style=dict(paddingLeft='0.5vw',paddingRight='0.5vw')),

                          dbc.Col([dbc.Card(dbc.CardBody([map_header,
                                                          dbc.Spinner([map_div], size="lg", color="primary",
                                                                      type="border",
                                                                      fullscreen=False)

                                                          ])
                                            , style=dict(backgroundColor='#f7f7f7'), id='card10',
                                            className='map-card'), html.Br()
                                   ], xl=dict(size=5, offset=0), lg=dict(size=6, offset=0),
                                  md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                  style=dict(paddingLeft='0.5vw',paddingRight='0.5vw')),

                          dbc.Col([dbc.Card(dbc.CardBody([word_cloud_header,
                                                          dbc.Spinner([word_cloud], size="lg", color="primary",
                                                                      type="border",
                                                                      fullscreen=False),topics_menu_div2

                                                          ])
                                            , style=dict(backgroundColor='#f7f7f7'), id='card11',
                                            className='map-card'), html.Br()
                                   ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                                  md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                  style=dict(paddingLeft='0.5vw',paddingRight='0.5vw')),

                          dbc.Col([dbc.Card(dbc.CardBody([donut_header,
                                                          dbc.Spinner([donut_div], size="lg", color="primary",
                                                                      type="border",
                                                                      fullscreen=False)

                                                          ])
                                            , style=dict(backgroundColor='#f7f7f7'), id='card12',
                                            className='map-card'), html.Br()
                                   ], xl=dict(size=3, offset=0), lg=dict(size=4, offset=0),
                                  md=dict(size=4, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                                  style=dict(paddingLeft='0.5vw', paddingRight='0.5vw'))

                        ],className='g-0')
                      ]

                     )




app.layout = html.Div([dbc.Spinner([html.Div(id='layout')],size="lg", color="primary", type="border", fullscreen=True,id='spinner')
,dcc.Location(id='url', refresh=True,pathname='/Dashboard')
                       ], style=dict(backgroundColor='white'), className='main',
                      id='main_div')

'''
setting the landing page url extension to /Dashboard and loading app.layout there
'''
@app.callback([Output('layout','children'),Output('spinner','delay_show')],Input('url','pathname'))
def landing_page(pathname):
    if pathname=='/Dashboard':
        return (main_layout,60000 )
    else:
        return (dash.no_update ,dash.no_update)


'''
updating the line chart depending on topic selected
'''
@app.callback(Output('date_chart','figure'),Input('topics_menu','value'))
def update_date_chart(selected_topic):
    fig=go.Figure()
    graph_data = df.copy()
    graph_data.set_index('created',inplace=True) # setting the index to 'created' column
    sent_dict = {'1': 'Negative', '2': 'Neutral', '3': 'Positive'} # mapping sentiment numbers to text values
    sent_colors= {'1': 'red', '2': '#e3a817', '3': 'green'} # mapping sentiment numbers to colors

    # checking if selected topic is not all topics ( user choosed one topic )
    if( selected_topic!='All Topics'):
        graph_data=graph_data[graph_data['topic']==selected_topic] # filtering dataframe based on that topic

    for i in range(1,4):
        data=graph_data[graph_data['sentiment']==str(i)] # looping through the data filtered with each sentiment
        data=data.resample('1D').count() # getting the count of tweets for each day

        # line chart

        fig.add_trace(
            go.Scatter(x=data.index, y=data['tweetId'].astype('int64'), mode='lines', name=sent_dict[str(i)],
                       marker_color=sent_colors[str(i)]
                       #, stackgroup='one'
                       ))

    fig.update_layout(
        xaxis_title='<b>Date<b>', yaxis_title='<b>Number of Tweets<b>',
        font=dict(size=14, family='Arial', color='black'), hoverlabel=dict(
            font_size=14, font_family="Rockwell", font_color='black', bgcolor='white'), plot_bgcolor='#f7f7f7',
        paper_bgcolor='#f7f7f7',
        xaxis=dict(

            tickwidth=2, tickcolor='#80ced6',
            ticks="outside",
            tickson="labels",
            rangeslider_visible=False
        ),margin=dict(l=0, r=0, t=30, b=0)
    )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    return fig

'''
updating the vertical bar chart depending on radio button selected
'''
@app.callback([Output('ver_bar_chart','figure'),Output('ver_bar_chart_header','children')],
              Input('location_filter','value'))
def update_ver_bar_chart(selected_location):
    # checking if user choosed countries or cities and set the loc parameter that will be sent to the charts.py function according to it
    if selected_location=='city':
        loc='Cities'

    elif selected_location=='country':
        loc='Countries'

    return (charts.create_ver_bar(df,selected_location), 'Top 5 {} With Tweets'.format(loc))

'''
updating the wordcloud depending on topic selected
'''
@app.callback(Output('word_cloud','src'),Input('topics_menu2','value'))
def update_word_cloud(selected_topic):

    dire=os.path.join(THIS_FOLDER, '{}.png'.format(selected_topic))

    encoded = base64.b64encode(open(dire, 'rb').read())

    return 'data:image/jpg;base64,{}'.format(encoded.decode())
if __name__ == '__main__':
    app.run_server(host='localhost',port=8044,debug=False,dev_tools_silence_routes_logging=True)