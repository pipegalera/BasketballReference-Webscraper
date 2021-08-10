from functions_app import *

st.markdown(" # :basketball: NBA Data Scraper :basketball:")
st.subheader('Web App by [Pipe Galera](https://www.pipegalera.com/)')



########################### Lists and Dictionaries ###########################

current_season = int(start_of_the_season_indicator()[5:])

seasons_dict, seasons_list =  get_seasons_dict(1950, current_season+1)


########################### Data Scraper ###############################

with st.form('Form'):
    selected_seasons = st.multiselect('NBA Seasons:', seasons_list, seasons_list[:22])
    selected_stats_type = st.selectbox('Data:', list(stats_dict.keys()))                                  
    submit = st.form_submit_button(label='Submit')

if submit:
    if selected_stats_type == 'Teams statistics': 
        with st.spinner('Loading...'):
            df = loading_teams_data(seasons_dict, selected_seasons)
        df_header = 'Team stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    elif selected_stats_type == 'Players salary (only available from 1990 on)': 
        with st.spinner('Loading...'):
            df = nba_salaries(seasons_dict, selected_seasons)
        df_header = 'Player stats for the ' + str(len(selected_seasons)) + ' selected seasons'
    else:
        with st.spinner('Loading...'):
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
