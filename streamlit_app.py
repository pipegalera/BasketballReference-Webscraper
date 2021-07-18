import streamlit as st
import pandas as pd
from functions_app import *

st.markdown(" # :basketball: NBA Data Scraper :basketball:")
st.subheader('Web App by [Pipe Galera](https://www.pipegalera.com/)')

<<<<<<< HEAD

=======
st.header('How does the app works?')
st.markdown("""
             1. 👇 Select the **NBA seasons**.

             2. ⛹️‍♀️ Choose among several **Player statistics** or **Team statistics**.

             3. 🖱️ Click **Show me the data!**

             4. 📂 Download clean player data in Excel or .csv format.
""" )

st.markdown("---")

########################### Seasons ###########################


seasons = {}
list_years = list(reversed(range(1950,2022)))
for year in list_years:
        key = str(year-1) + '-' + str(year)
        seasons[key] = year

seasons_list = list(seasons.keys())

st.subheader('1. Select NBA seasons')

selected_seasons = st.multiselect('NBA Seasons:',
                                       seasons_list,
                                       seasons_list[:22])

########################### Players ###########################

st.subheader('2. Choose the kind of Player statistics')

# Options
players_stats = {'Total stats': 'totals',
              'Stats per game': 'per_game',
              'Stats per 36 minutes': 'per_minute',
              'Stats per 100 possesions': 'per_poss',
              'Adavanced stats': 'advanced'}


selected_type = st.selectbox('Player statistics:',
                                     list(players_stats.keys()))


@st.cache
def loading_players_data(selected_seasons, selected_type):
    # User selections
    list_seasons = []
    for i in selected_seasons: list_seasons.append(seasons.get(i))
    type = players_stats.get(selected_type)


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
        season = [d for d in url if d.isdigit()]
        season = ''.join(season)
        part_df["Season"] = str(int(season)-1) + "/" + str(int(season))[2:]
>>>>>>> c3f59916374434a0e517f8dfcb3b2e1fb4ea6111

########################### Lists and Dictionaries ###########################

seasons_dict, seasons_list =  get_seasons_dict(1950, 2022)

stats_dict = {'Players total stats': 'totals',
              'Players stats per game': 'per_game',
              'Players stats per 36 minutes': 'per_minute',
              'Players stats per 100 possesions': 'per_poss',
              'Players adavanced stats': 'advanced',
              'Players salary (only available from 1990 on)': 'salaries',
              'Teams statistics': 'teams'}

########################### Data Scraper ###############################

with st.form('Form'):
    selected_seasons = st.multiselect('NBA Seasons:', seasons_list, seasons_list[:22])
    selected_stats_type = st.selectbox('Data:', list(stats_dict.keys()))                                  
    submit = st.form_submit_button(label='Submit')

if submit:
    if selected_stats_type == 'Teams statistics': 
        df = loading_teams_data(seasons_dict, selected_seasons)
        df_header = 'Team stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    elif selected_stats_type == 'Players salary (only available from 1990 on)': 
        df = nba_salaries(seasons_dict, selected_seasons)
        df_header = 'Player stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    else:
        df = loading_players_data(seasons_dict, stats_dict, selected_seasons, selected_stats_type)
        df_header = 'Player stats for the ' + str(len(selected_seasons)) + ' selected seasons'

    st.subheader(df_header)
    st.write(df)
    st.markdown("**Source:** Real-time scraped from [Basketball-reference.com](https://www.basketball-reference.com/). Salaries data comes from [Hoopshype.com](https://hoopshype.com/salaries/)")
    st.markdown("---")


    column1, column2, column3 = st.beta_columns(3)
    with column2:
        st.markdown(link_csv(df), unsafe_allow_html=True)
        st.markdown(link_excel(df), unsafe_allow_html=True)

else:
    pass
<<<<<<< HEAD
=======

st.markdown("---")

########################### Teams ###########################

st.subheader('2. Team statistics')

@st.cache
def loading_teams_data(selected_seasons):
    # User selections
    list_seasons = []
    for i in selected_seasons: list_seasons.append(seasons.get(i))

    # Get URLs for the selected seasons and statistics type
    url_list = []
    for season in list_seasons:
        url = "https://www.basketball-reference.com/leagues/NBA_{season}_ratings.html".format(season=season)
        url_list.append(url)

    # Screape data
    df = pd.DataFrame()
    for url in url_list:
        part_df = pd.read_html(url, header = 1)[0]

        # Indicate year
        year = [d for d in url if d.isdigit()]
        year = ''.join(year)
        part_df["Season"] = year

        # Append all the years
        df = df.append(part_df, ignore_index = True)

        # Drop empty columns
        df = df.drop(columns = ['Rk'])

        # Fill nans (Only ORtg or DRtg from 1983 on)
        df = df.fillna(0)
        df = df.apply(pd.to_numeric, errors = 'ignore')

    return df


col1, col2, col3 = st.beta_columns(3)
with col2:
    st.markdown(' ')
    st.markdown(' ')
    button_teams = st.button("3. Show me the teams data!")

if button_teams:
    df2 = loading_teams_data(selected_seasons)
    df2_header = 'Team stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    st.subheader(df2_header)
    st.write(df2)
    st.markdown("**Source:** Real-time scraped from [Basketball-reference.com](https://www.basketball-reference.com/).")
    st.markdown("---")
    st.subheader('**4. Download the data** in the most convinient format for you: ')

    links1, links2, links3 = st.beta_columns(3)
    with links2:
        st.markdown(link_csv(df2), unsafe_allow_html=True)
        st.markdown(link_excel(df2), unsafe_allow_html=True)

else:
    pass

>>>>>>> c3f59916374434a0e517f8dfcb3b2e1fb4ea6111
