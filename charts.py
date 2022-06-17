import plotly.express as px
import plotly.graph_objects as go
import re
import string
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize




'''
horizontal bar chart
'''

def create_hor_bar(df):
    fig=go.Figure()
    graph_data = df.copy()
    sent_dict = {'1': 'Negative', '2': 'Neutral', '3': 'Positive'}
    sent_colors= {'1': 'red', '2': '#e3a817', '3': 'green'}
    c=3
    # looping through each filtered data with sentiment and make the barchart and stack all charts
    for i in range(1,4):
        data=graph_data[graph_data['sentiment']==str(c)]
        data=data.groupby('topic',sort=False)['sentiment'].count() # grouping by topic and get count of sentiments for each
        data.sort_values(inplace=True, ascending=False) # sorting descending

        # create the bar chart
        fig.add_trace(go.Bar(name=sent_dict[str(c)], x=data.astype('int64'), y=data.index,
                             marker_color=sent_colors[str(c)],orientation='h',text=data.astype('int64'),
               textposition='inside', textfont=dict(
                size=13,

            ))
                      )
        c-=1

    fig.update_layout(
            xaxis_title='<b>No. of Sentiments<b>', yaxis_title=None,
          #'<b>Topic<b>',
            font=dict(size=14, family='Arial', color='black'), hoverlabel=dict(
                font_size=14, font_family="Rockwell"), plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',barmode='stack',margin=dict(l=0, r=0, t=30, b=0)

        )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black',visible=False)
    fig.update_yaxes(showgrid=False, showline=False, zeroline=False, linecolor='black',autorange="reversed",visible=True,showticklabels=True)

    return fig

'''
vertical bar chart
'''
def create_ver_bar(df,location):
    graph_data = df.copy()
    graph_data=graph_data.groupby(location,sort=False)['tweetId'].count() # grouping by city or country column and get tweets count for each
    graph_data.sort_values(inplace=True, ascending=False)
    graph_data = graph_data.nlargest(5)  # gettting the largest 5 countries or cities with tweets
    fig=go.Figure()
    fig.add_trace(go.Bar(x=graph_data.index, y=graph_data.astype('int64'),
                         marker_color='#1dabdd', text=graph_data.astype('int64'),
                         textposition='auto', textfont=dict(
            size=13,color='black'

        ))
                  )

    fig.update_layout(
            xaxis_title='<b>{}<b>'.format(location.capitalize()), yaxis_title='<b>Number of Tweets<b>',
            font=dict(size=13, family='Arial', color='black'), hoverlabel=dict(
                font_size=14, font_family="Rockwell"), plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',margin=dict(l=0, r=0, t=20, b=0)

        )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black',visible=True)
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black',visible=True,showticklabels=True)

    return fig

'''
Map
'''
def create_countries_map(df):

    map_df = df.groupby(['country', 'country_lon', 'country_lat'])['tweetId'].count() # grouping by country and coordinates

    map_df = map_df.reset_index().sort_values('tweetId', ascending=False)

    map_df['size']=10   # adding size column to be used in map figure

    # creating the map figure with continous color scale that reflects the number of tweets
    fig = px.scatter_mapbox(map_df, lat="country_lat", lon="country_lon",text='country',custom_data=['country','tweetId'],
                            size='size',
                   size_max=12, zoom=0,
                            labels={'tweetId': '<b>No. Tweets<b>'}
                           , color="tweetId",color_continuous_scale=px.colors.sequential.Turbo,
                            hover_data={"country": True,"country_lon": False,"country_lat": False,
                                        "tweetId": True,'size':False}
                            )

    fig.update_layout(mapbox_style='open-street-map', mapbox_center_lon=21.9877132, mapbox_center_lat=38.9953683,
                       mapbox_zoom=0)
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, hoverdistance=2, uirevision='func',
                       clickmode='event+select', hovermode='closest',plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7')
    fig.update_geos(fitbounds="locations",scope='world')

    return fig



def clean_data(text):
    # removing HTML special entities (e.g. &amp;)
    text = re.sub(r'\&\w*;', '', text)

    # removing url
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b', '', text)

    # text = re.sub(r'#[^\s]+','', text)

    # removing @username
    text = re.sub(r'@[^\s]+', '', text)

    return text


# Apply function on tweets

def remove_puncts(text):
    puncts = string.punctuation
    # return text.translate(str.maketrans('', '', puncts))
    text = re.sub('[' + puncts + ']+', ' ', text)

    text = re.sub(r'[^\w\s]', ' ', text)  # removing repeating punctuations
    return text



def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))

    return " ".join([word for word in str(text).split() if word not in stop_words])


# Apply function on tweets

def processed_tweet(text):
    # Remove whitespace (including new line characters)
    text = re.sub(r'\s\s+', ' ', text)

    # Remove single space remaining at the front of the tweet.
    text = text.lstrip(' ')

    # Remove words with 2 or fewer letters
    text = re.sub(r'\b\w{1,2}\b', '', text)

    # Replacing 2 or more consecutive whitespaces with a single one
    text = re.sub(r' {2,}', ' ', text)

    text = re.sub(r'[’]', '', text)  # text = re.sub(r'[’]s\b', '', text)

    return text

def cleaning_numbers(text):
    return re.sub('[0-9]+', '', text)


def tokenize(text):
    return word_tokenize(text)

