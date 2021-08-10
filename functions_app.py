import pandas as pd
import base64
from io import BytesIO
import streamlit as st
from datetime import date

teams_dict = {
    'AND': 'Anderson Packers', 
    'ATL': 'Atlanta Hawks',
    'BLB': 'Baltimore Bullets', 
    'BOS': 'Boston Celtics',
    'BRK': 'Brooklyn Nets',
    'BUF': 'Buffalo Braves', 
    'CAP': 'Capital Bullets', 
    'CHA': 'Charlotte Bobcats',
    'CHH': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CHO': 'Charlotte Hornets',
    'CHP': 'Chicago Packers', 
    'CHS': 'Chicago Stags', 
    'CHZ': 'Chicago Zephyrs', 
    'CIN': 'Cincinnati Royals', 
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'FTW': 'Fort Wayne Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'INO': 'Indianapolis Olympians', 
    'KCK': 'Kansas City Kings', 
    'KCO': 'Kansas City-Omaha Kings', 
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIH': 'Milwaukee Hawks', 
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'MNL': 'Minneapolis Lakers', 
    'NJN': 'New Jersey Nets',
    'NOH': 'New Orleans Hornets',
    'NOJ': 'New Orleans Jazz', 
    'NOK': 'New Orleans/Oklahoma City Hornets',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'NYN': 'New York Nets', 
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'PHW': 'Philadelphia Warriors',
    'POR': 'Portland Trail Blazers',
    'ROC': 'Rochester Royals', 
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'SDC': 'San Diego Clippers', 
    'SDR': 'San Diego Rockets', 
    'SEA': 'Seattle SuperSonics',
    'SFW': 'San Francisco Warriors',
    'SHE': 'Sheboygan Red Skins', 
    'SLH': 'St. Louis Hawks',
    'STB': 'St. Louis Bombers', 
    'SYR': 'Syracuse Nationals', 
    'TOR': 'Toronto Raptors',
    'TOT': 'Combination of different team stats',
    'TRI': 'Tri-Cities Blackhawks', 
    'UTA': 'Utah Jazz',
    'VAN': 'Vancouver Grizzlies',
    'WAS': 'Washington Wizards',
    'WAT': 'Waterloo Hawks', 
    'WSB': 'Washington Bullets',
    'WSC': 'Washington Capitols', 
    } 

teams_dict_inverted = dict(zip(teams_dict.values(), teams_dict.keys()))

def start_of_the_season_indicator():
    """
    If before Oct 19:
         current ended season
    If August:
         next starting season
    """
    if (date.today().month < 10) & (date.today().day < 10):
        return (str(date.today().year - 1) + str("-") + str(date.today().year))
    else:
        return (str(date.today().year) + str("-") + str(date.today().year + 1))

def start_of_the_free_agency_indicator():
    """
    If before August 4th:
         salaries current ended season
    If August 4th on:
         salaries next starting season
    """
    if (date.today().month < 8) & (date.today().day < 4):
        return (str(date.today().year - 1) + str("-") + str(date.today().year))
    else:
        return (str(date.today().year) + str("-") + str(date.today().year + 1))


def get_seasons_dict(from_season, to_season):
        seasons = {}
        list_years = list(reversed(range(from_season, to_season)))
        for year in list_years:
                key = str(year-1) + '-' + str(year)
                seasons[key] = year

        seasons_list = list(seasons.keys())

        return seasons, seasons_list

@st.cache(show_spinner=False)
def loading_players_data(seasons_dict, stats_dict, selected_seasons, selected_stats_type):
    # Store the key of the selected seasons
    keys_seasons = []
    for i in selected_seasons: 
        keys_seasons.append(seasons_dict.get(i))

    # Store the key of the selected statistic
    key_stats_type = stats_dict.get(selected_stats_type)

    # Get URLs for the selected seasons and statistics type
    url_list = []
    for season in keys_seasons:
        url = "https://www.basketball-reference.com/leagues/NBA_{season}_{type}.html".format(season=season, type=key_stats_type)
        url_list.append(url)


    # Screape data
    df = pd.DataFrame()
    for url in url_list:
        part_df = pd.read_html(url, header = 0)[0]

        # Indicate year
        season = [d for d in url if d.isdigit()]
        season = ''.join(season)
        part_df["Season"] = str(int(season)-1) + "/" + str(int(season))[2:]

        # Append all the years
        df = df.append(part_df, ignore_index = True)

    # Drop duplicates and empty columns
    df = df.drop(df[df['Age'] == 'Age'].index)
    df = df.drop(columns = ['Rk'])
    df = df.dropna(how = 'all', axis = 'columns')

    # Tidy data
    df = df.apply(pd.to_numeric, errors = 'ignore').fillna(0)
    df["Player"] = df["Player"].apply(lambda x: x.replace('*', ''))
    
    # Create a column with the full name of the team
    team_full = df['Tm'].map(teams_dict)
    df.insert(3, "Team", team_full)

    df = df.sort_values(by = ["Season", "Team"], ascending = False)
    df = df.reset_index(drop = True)

    return df

@st.cache(show_spinner=False)
def loading_teams_data(seasons_dict, selected_seasons):
    # Store the key of the selected seasons
    keys_seasons = []
    for i in selected_seasons: 
        keys_seasons.append(seasons_dict.get(i))

    # Get URLs for the selected seasons and statistics type
    url_list = []
    for season in keys_seasons:
        url = "https://www.basketball-reference.com/leagues/NBA_{}_ratings.html".format(season)
        url_list.append(url)

    # Screape data
    df = pd.DataFrame()
    for url in url_list:
        part_df = pd.read_html(url, header = 1)[0]

        # Indicate year
        season = [d for d in url if d.isdigit()]
        season = ''.join(season)
        part_df["Season"] = str(int(season)-1) + "/" + str(int(season))[2:]

        # Append all the years
        df = df.append(part_df, ignore_index = True)

        # Drop empty columns
        df = df.drop(columns = ['Rk'])

    # Fill nans (eg. Only ORtg or DRtg from 1983 on)
    df = df.fillna(0)
    df = df.apply(pd.to_numeric, errors = 'ignore')

    # Create a column with the abbreviation name of the team
    team_abv = df['Team'].map(teams_dict_inverted)
    df.insert(1, "Tm", team_abv)

    df = df.sort_values(by = ["Season", "W/L%"], ascending = False)
    df = df.reset_index(drop = True)

    return df
    
@st.cache(show_spinner=False)
def nba_salaries(seasons_dict, selected_seasons):
    # Store the key of the selected seasons
    keys_seasons = []
    for i in selected_seasons: 
        keys_seasons.append(seasons_dict.get(i))

    # List of URLs
    list_urls = []
    for season in selected_seasons:
        if season == start_of_the_free_agency_indicator():
            url = 'https://hoopshype.com/salaries/players/'
            list_urls.append(url)
        else:
            url = 'https://hoopshype.com/salaries/players/{}'.format(season)
            list_urls.append(url)

    # Create a DataFrame that we will add the info in the url list by loop
    df = pd.DataFrame()

    # Salaries 
    for url in list_urls:
        if url == 'https://hoopshype.com/salaries/players/':
            salary = pd.read_html(url, header = 0)[0].iloc[:,1:3]
            # Add a column indicating the season of the salary
            salary["Season"] = salary.columns[1]
            # Rename the previous column name with just "Salary"
            salary.rename(columns={salary.columns[1]: "Salary"}, inplace = True)

            df = df.append(salary, ignore_index = True)

        else:
            salary = pd.read_html(url, header = 0)[0].iloc[:,1:]
            # Add a column indicating the season of the salary
            salary["Season"] = salary.columns[1] 
            # Rename the previous column name with just "Salary"
            salary.rename(columns={salary.columns[1]: "Salary", 
                                   salary.columns[2]: "Salary adjusted by inflation"}, 
                          inplace = True)

            df = df.append(salary, ignore_index = True)

    # Tidy the dataset
    df = df.replace(['\$', ','], '', regex=True)
    df = df.apply(pd.to_numeric, errors = 'ignore').fillna(0)
    df = df.sort_values(by = ["Season", "Salary"], ascending = False)
    
    df = df.reset_index(drop = True)
    
    return df


# To donwload the data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def link_excel(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
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

















































