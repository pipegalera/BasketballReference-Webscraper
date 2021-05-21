# @Author: pipegalera
# @Date:   2020-10-04T21:40:56+02:00
# @Last modified by:   pipegalera
# @Last modified time: 2020-10-20T12:42:39+02:00



import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import time

st.markdown(" # :basketball: NBA Players stats Scraper :basketball:")
st.subheader('Web App by [Pipe Galera](https://www.pipegalera.com/)')


# Options
stats_type = {'Total stats': 'totals',
              'Stats per game': 'per_game',
              'Stats per 36 minutes': 'per_minute',
              'Stats per 100 possesions': 'per_poss',
              'Adavanced stats': 'advanced'}

seasons = {}
list_years = list(reversed(range(1950,2022)))
for year in list_years:
    if year < 2021:
        key = str(year-1) + '-' + str(year)
        seasons[key] = year
    if year >= 2021:
        seasons[year] = year

seasons_list = list(seasons.keys())

# Sidebar
st.header('How does the app works?')
st.markdown("""
             1. 👇 Select the **seasons** and type of **statistics** (*total stats*, *per game*, *advanced stats*...)

             2. 🖱️ Click **Show me the data!**

             3. ⛹️‍♀️ Download clean player data in Excel or .csv format.
""" )

st.markdown("---")


selected_seasons = st.multiselect('NBA Seasons:',
                                       seasons_list,
                                       seasons_list[:22])
selected_type = st.selectbox('Kind of statistics:',
                                     list(stats_type.keys()))


@st.cache
def load_data(selected_seasons, selected_type):
    # User selections
    list_seasons = []
    for i in selected_seasons: list_seasons.append(seasons.get(i))
    type = stats_type.get(selected_type)


    # Get URLs for the selected seasons and statistics type
    url_list = []
    for season in list_seasons:
        url = "https://www.basketball-reference.com/leagues/NBA_{season}_{type}.html".format(season=season, type=type)
        url_list.append(url)


    # Screape data
    df = pd.DataFrame()
    for url in url_list:
        part_df = pd.read_html(url, header = 0)[0]

        # Indicate year
        year = [d for d in url if d.isdigit()]
        year = ''.join(year)
        part_df["Season"] = year

        # Append all the years
        df = df.append(part_df, ignore_index = True)

    # Drop duplicates and empty columns
    df = df.drop(df[df['Age'] == 'Age'].index)
    df = df.drop(columns = ['Rk'])
    df = df.dropna(how = 'all', axis = 'columns')

    # Fill nans and turn data into numeric
    df = df.fillna(0)
    df = df.apply(pd.to_numeric, errors = 'ignore')

    return df

col1, col2, col3 = st.beta_columns(3)
with col2:
    st.markdown(' ')
    st.markdown(' ')
    button = st.button("Show me the data!")


df = load_data(selected_seasons[:2], selected_type)


# To donwload the data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def link_excel(df):
    val = to_excel(df)
    b64 = base64.b64encode(val)

    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="data.xlsx">Download Excel file</a>'

def link_csv(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'

if button:
    df = load_data(selected_seasons, selected_type)
    df_header = 'Player stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    st.header(df_header)
    st.write('Number of rows in the data: ' + str(df.shape[0]) + ', that correspond to stats of ' + str(len(df.Player.unique())) + ' different Players')
    st.write(df)
    st.write('**Note**: a Player name followed by ***** indicates member of the Hall of Fame.')
    st.markdown("**Source:** Real-time scraped from [Basketball-reference.com](https://www.basketball-reference.com/).")
    st.markdown("---")
    st.header('**Download the data** in the most convinient format for you: ')

    links1, links2, links3 = st.beta_columns(3)
    with links2:
        st.markdown(link_csv(df), unsafe_allow_html=True)
        st.markdown(link_excel(df), unsafe_allow_html=True)

else:
    pass
