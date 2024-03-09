#team_details, player_stats

"""
Created on Sun Aug 13 10:44:36 2023

@author: mawrencela
"""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import json

pd.set_option('max_info_rows', 115)
pd.set_option('max_info_columns', 115)

own_palette = ["#f67088", "#f77367", "#f37932", "#db8831", "#ca9131", "#bb9731","#ad9c31", "#9ea131", "#8ea531", "#77aa31", "#4fb031", "#32b15c", "#33b07a", "#34ae8c", "#34ad99", "#35aca4", "#36abae", "#37aab9", "#38a8c5", "#39a6d4", "#3ba3ec", "#6e9af4", "#9491f4", "#b186f4", "#cc79f4", "#e766f4", "#f45fe3", "#f565cc", "#f569b7", "#f66da2"]

st.set_page_config(layout="wide")

mypath = "/Users/mawrencela/Desktop/datascience/EuropeanSoccer/"

team_info = pd.read_csv(mypath + 'github_team_info.csv')
team_all=pd.read_csv(mypath +'github_team_all.csv')
defence_info=pd.read_csv(mypath + 'github_defence_info.csv')
github_world_path = mypath + 'github_geoworld.geojson'
world_path = mypath + 'github_geoworld.geojson'
team_details = pd.read_csv(mypath + 'github_team_details.csv')
player_stats = pd.read_csv(mypath + 'github_player_stats.csv')
with open(world_path) as f:
    geo_world = json.load(f)

num_cols = team_info.select_dtypes(include = 'number').columns
num_cols = list(num_cols)
cat_cols = team_info.select_dtypes(include = [object,'category']).columns
cat_cols = list(cat_cols)
team_name_cols = ['team_long_name','country_name','league_name']

category_order_dict = {'chanceCreationCrossingClass':['Lots','Normal','Little'],
                       'buildUpPlayPassingClass':['Long','Mixed','Short'],
                       'buildUpPlaySpeedClass':['Fast','Balanced','Slow'],
                       'buildUpPlayDribblingClass':['Lots','Normal','Little'],
                       'buildUpPlayPositioningClass':['Free','Organized'],
                       'chanceCreationPassingClass':['Risky','Normal','Safe'],
                       'chanceCreationPositioningClass':['Free Form','Organized'],
                       'chanceCreationShootingClass':['Lots','Normal','Little'],
                       'defencePressureClass':['High','Medium','Deep'],
                       'defenceAggressionClass':['Press','Contain','Double'],
                       'defenceTeamWidthClass':['Wide','Normal','Narrow'],
                       'defenceDefenderLineClass':['Offside Trap','Cover']}

pretty_names_cat = {'country_name':"Country",'team_long_name':'Team Name','buildUpPlaySpeedClass':'Build Up Play Speed (class)', 'buildUpPlayDribblingClass':'Build Up Play Dribbling (class)','buildUpPlayPassingClass':'Build Up Play Passing (class)','buildUpPlayPositioningClass':'Build Up Play Positioning (class)','chanceCreationPassingClass':'Chance Creation Passing (class)','chanceCreationCrossingClass':'Chance Creation Crossing (class)','chanceCreationShootingClass':'Chance Creation Shooting (class)','chanceCreationPositioningClass':'Chance Creation Positioning (class)','defencePressureClass':'Defence Pressure (class)','defenceAggressionClass':'Defence Aggression (class)','defenceTeamWidthClass':'Defence Team Width (class)','defenceDefenderLineClass':'Defence Line (class)','favored_cuttoff':'Favored CutOff'}
pretty_names_num = {'favored':'Team Favorability Rating','buildUpPlaySpeed':'Build Up Play Speed','buildUpPlayDribbling':'Build Up Play Dribbling','buildUpPlayPassing':'Build Up Play Passing','chanceCreationPassing':'Chance Creation Passing','chanceCreationCrossing':'Chance Creation Crossing','chanceCreationShooting':'Chance Creation Shooting','defencePressure':'Defence Pressure','defenceAggression':'Defence Aggression','defenceTeamWidth':'Defence Team Width','avg_defence_stats':'Average Defensive Stats'}
pretty_names_all = pretty_names_cat.copy()
pretty_names_all.update(pretty_names_num)


with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis', 'Analysis: Build Up Play', 'Analysis: Chance Creation','Analysis: Defence', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'box', 'megaphone-fill', 'bug','building','dice-5', 'shield-fill-exclamation', 
		'check2-circle'],
		default_index = 0,
		)

if selected=='Abstract':
    st.title("Abstract")
    st.markdown('With a long history that traces back to the 19th century, European Football has an influence that extends beyond the simple sporting spectacle. It influences social culture, politics, and even the economy. Madrid, Spain, gained an economic benefit of around 60 million to 70 million euros by hosting the Champions League final alone in 2019. Even one simple match can generate an unbelievable economic impact, showcasing how influential football is as a sport and why it’s worth analyzing.')
    st.markdown('''This case study aims to look in-depth at all of the mainstream football leagues around Europe and at what level each team is rated in the league they play in. European Football is known for its high level and high commercialization; that's why it's the best sample to be analyzed and is most likely to lead to a justified conclusion.''')
    st.markdown('The end goal is to elucidate the scientific factors that delineate good and bad football teams, offering valuable insights to fans, coaches, and players alike. Through a detailed examination of technical factors, our conclusion will synthesize key takeaways, offering actionable advice and strategic considerations that can influence the development of more effective and cohesive teams."')

if selected=="Background Information":
    st.title("Background Information")
    st.markdown('''European Football is considered the origin of modern football, with England being its leader, credited as the 'Mother of Football.' In 1863, England established the first official football association in the world. After the creation of the first official governing body of the sport, football quickly differentiated from Rugby, adopting standardized rules. Once the rules were standardized, Football began to spread across the British Isles and eventually reached the rest of Europe. Many European countries, such as Germany, Spain, France, and many more, established their own leagues and created their own associations.''')
    st.markdown("This dataset provides data on different football teams and players in Europe. For player data, it contains specific information for evaluating how strong the player is, such as speed, acceleration, strength, and many more, rated from 0 to 100. For team data, it includes information such as matches they have participated in, the betting odds before the game, and the league/country they belong to. In this case study, the data will aim to find out how many times each team has been favored by the betting companies, and separate them into different levels, to give fans a better understanding of the level of play of the players, but more importantly, provide bookmakers with better opening values.")
    st.markdown("This dataset offers an opportunity to examine how the ratings of teams and players affect their win rate and at what level each team is positioned. This will provide a better understanding for football fans of where their supported team stands, and serve as a reference for future discussions in the field.")
    st.markdown('Over the past decade, football teams have experienced notable shifts in playing styles, influenced by technological advancements, data analytics, and the global exchange of tactical ideas. Despite these changes, the fundamental tactical trends—such as possession-based play, high pressing, and quick transitions—have remained constant, showcasing an adherence to core principles while adapting to modern developments. Thus, this case study reveals a general trend that is still applicable today, despite the dataset being relatively old.')
    ###Include cites!! Include bet365
    st.markdown('''In this case study, the betting odds provided by betting companies are crucial, as they are the only possible way to evaluate which team is favored more by the betting companies and the public. The number of times being favored by the betting odds demonstrates the general level of a football team. In this case study, a betting company named Bet365 was used as the reference. Bet365 is one of the world's leading online gambling companies, offering a wide range of betting options across various sports and events, including football. Founded in 2000 by Denise Coates in Stoke-on-Trent, England, Bet365 has grown to become a global presence in the betting industry. Due to its credibility, reputation, and the extensive amount of data in the dataset, it was selected for use as the reference."''')
    st.dataframe(team_details)
    
if selected=="Data Cleaning":
    st.title('Data Cleaning')
    st.subheader('Team Stats Cleaning')
    st.markdown("In order to achieve the goal of ranking the teams, there will be several information that we need to evaluate each team through multiple perspectives. While exploring the dataset of matches, which records specific details of each match, it was discovered that it included the odds of winning for the home/away team in each match. Through this information, we could find out how many times a team was favoured and how often it was favoured, providing a general idea of the level.")
    st.markdown('Beginning with the betting odds, we need to first find out which betting company has the highest credibility and most information about the odds in this dataset. If there are not enough data provided or the company is not reliable, it would affect our analysis.')
    st.markdown('To find out which betting company has the most data for the matches, the “match” dataset will be used. The following code is used to find out how many NA values there are for the betting odds provided by different betting companies:')
    st.code('''match[‘Name of Betting Company'].value_counts(dropna=False)''')
    st.markdown('This code shows the value count for each value provided by the betting company, including how many of them are missing (NA). After looking through all of the data, it is found that “B365H” has the least amount of NA values, being 3387. After conducting research, “B365H” could be considered as a justifies source for the betting odds.')
    st.markdown('What needs to be done next is find out how many times each team is favoured by the betting odds. How betting odds in football work is the lower the number is, the likelier the team is to win. That is because the number is the value in return per unit of currency if the correct predictions were made through betting. In this case, the higher the number is, the unlikelier the team is to win, as the reward is higher for taking a higher risk. The following code is used to find out how many times each team was favoured and rank them by the result:')
    st.code('''match['favorite']=np.where(match['B365A'].isnull(),np.nan,np.where(match['B365H'] <= match['B365A'],
        match['home_team_api_id'],match['away_team_api_id']))''')
    st.code('''team_favorites=match['favorite'].value_counts().reset_index().rename({'favorite':'team_api_id','count':'favored'},axis=1)''')
    st.code('''team_favorites = pd.concat([team_favorites,pd.DataFrame([[108893,0]],columns = ['team_api_id','favored'],index=[259])])''')
    st.markdown('The code creates a new column "favorite" to store the team that was favored to win each match (home or away team). Then, it counts how many times each team was favored and ranks them. The counting is done through comparing the betting odds between the home and away team, if the home team has a lower value than the favored column gets added by 1 for that team, vice versa. If a team was never favored, it adds a row for that team with a count of 0')
    st.markdown("The following code processes and organizes data related to football matches, teams, and players. Initially, it creates a new DataFrame, match_teams, consisting of columns for the first home player and home team, while simultaneously removing any missing values. The player IDs are then converted to integers, and the columns are renamed to 'player_api_id' and 'team_api_id'. Following this, any duplicate rows within match_teams are removed.")    
    st.code('''match_teams = match[['home_player_1','home_team_api_id']].dropna().copy()
match_teams['home_player_1'] = match_teams['home_player_1'].astype(int)
match_teams.rename({'home_player_1':'player_api_id','home_team_api_id':'team_api_id'},axis = 1,inplace = True)
match_teams.drop_duplicates()''')
    st.markdown("In addition, the 'date' column in the match DataFrame is converted to datetime format, and the DataFrame is sorted based on this date. A dictionary, team_code, is then created to map team API IDs to their respective long names. Finally, two new columns, 'home_team' and 'away_team', are added to the match DataFrame, utilizing the team_code dictionary to substitute team API IDs with their corresponding long names.")
    st.code('''mmatch['date'] = pd.to_datetime(match['date'])
match.sort_values('date',inplace = True)
team_code = {code:team for code,team in zip(team['team_api_id'],team['team_long_name'])}
match['home_team'] = match['home_team_api_id'].map(team_code)
match['away_team'] = match['away_team_api_id'].map(team_code)''')

    st.markdown('Next, the useful parts of each dataframe that had been used above will be merged into one big dataset that will be used to make graphs throughout the entire case study. It will be named team_details and team_all since it includes all of information that are required.')
    st.code('''team_rankings = pd.merge(team,team_favorites,on='team_api_id',
            how='inner').sort_values('favored',ascending = False)
team_rankings.isnull().sum()
            team_details = pd.merge(league[['league_id','name']],match_league,
            on='league_id').drop_duplicates(subset='team_api_id')
team_details = team_details.rename(columns={'name':'league_name'})
team_details = pd.merge(team_details,country,on='country_id')
team_details = team_details.rename(columns={'name':'country_name'})
team_details = pd.merge(team_details,team_rankings,on='team_api_id')
team_details''')
    st.markdown('Through the merging process, we get the league ids and country ids matched with the league name and country ids, knowing which league and country each team belongs to. After that, team_rankings, which includes all of the important data such as "favored" that was just calculated, will be merged into team_details to make it a complete dataset with all of the details that are useful and will be needed.')
    st.markdown('The Because team_details are still missing several columns, we will first merge team_details with several other columns of other dataframes to make it include everything that might be helpful in the future analysis process. We will name this new dataframe team_all.')
    st.code('''team_all = pd.merge(team_rankings[['team_api_id','favored_cutoff']],
            team_details,on=['team_api_id','favored_cutoff'])
team_all = pd.merge(team_all[['team_api_id','favored','favored_cutoff','team_long_name',
                              'team_short_name']],team_attributes,on='team_api_id')''')
    st.code('''team_all['team_api_id'].nunique()''')
    st.markdown('When compared to team_details, during the merging process of team_all there are nine teams that are dropped. We need to find out which nine teams are dropped in the process. We could find all of the unique values of team_api_id in team_rankings, team_details, and team_attributes and merge them together and compare it to the final team all to see which teams are missing.')
    st.markdown('''If it is necessary to retrieve them is important. np.setdiff1d was used to find the team_api_id that were in team_details but not in team_attributes. The nine teams missing in team_attributes were found and displayed. It turned out that these teams were recorded in the "teams" dataframe, but not it the "team_attributes" dataframe, which means we don't have any statistics for them, and it's impossible to retrieving them. Understanding that, we know that there are no errors that had occured. After doing research on the three leagues the missing teams belong to, we found out that there is either a major change to the league at some point (for example changing it's name or amount of teams in the league) or the team had been relegated multiple times.''')
    st.code('''missing_team_api_ids = np.setdiff1d(team_details['team_api_id'],
            team_attributes['team_api_id'])
team_details[team_details['team_api_id'].isin(missing_team_api_ids)]''')
 
    st.subheader('Player Stats Cleaning')
    st.markdown('Finally, examinating player stats is necissary to understand why some of my original hypothesis were not as expected. This is used to aggregate players within a team in order to gain a deeper insight into more of the team statistics.')
    st.code('''match_teams = match[['home_player_1','home_team_api_id']].dropna().copy()
match_teams['home_player_1'] = match_teams['home_player_1'].astype(int)
match_teams.rename({'home_player_1':'player_api_id','home_team_api_id':'team_api_id'},axis = 1,inplace = True)
match_teams.drop_duplicates()''')
    st.markdown('The above piece of code focuses on home players and their corresponding teams from football matches. Initially, it selects and cleans data related to the first home player and the home team, removing any rows with missing values. It then ensures that player IDs are treated as integers for consistency. This part also renames the selected columns to more generic terms, making the data easier to understand and work with. It then removes any duplicate entries to ensure each row represents a unique player-team pairing. The aim is to create a cleaned and standardized DataFrame where each row links a player to their team, based on home match data, facilitating further analysis or processing of player-team relationships within the dataset.')
    st.code('''match_teams = pd.melt(match.filter(regex = 'home_team_api_id|home_player_\d+'),id_vars = 'home_team_api_id',value_name = 'player_api_id').dropna().drop_duplicates()
match_teams['player_api_id'] = match_teams['player_api_id'].astype(int)
match_teams.drop('variable',axis = 1,inplace = True)
match_teams.rename({'home_team_api_id':'team_api_id'},axis = 1,inplace = True)
match_teams = match_teams.drop_duplicates()
match_teams''')
    st.markdown('Now, we should reshape the "match" dataframe and collect all of the player IDs and team IDs to match them using the pd.melt function. Then the missing values and duplicates are removed, as well as the variable column generated by melt, and renames home_team_api_id to team_api_id. Finally, it ensures that only unique rows are retained, preparing a clean list of matches with players associated with their home teams.')
    st.code('''player_team_info = pd.merge(player[['player_api_id','player_name','birthday','height','weight']],match_teams,on = 'player_api_id',how = 'left')
player_team_info = pd.merge(player_team_info,team[['team_api_id','team_long_name','team_short_name']],on = 'team_api_id',how = 'left')
player_team_info.info()''')
    st.markdown('''This part merges the previously prepared match_teams DataFrame with player information (including name, birthday, height, and weight) and team names, adding detailed attributes to each player-team pairing. It uses left joins to ensure all player entries are included, even if they don't match a team in match_teams, and similarly for team names, resulting in a comprehensive dataset of player-team associations with personal and team details.''')
    st.code('''player_object = player_attributes_plus.groupby(['player_api_id','player_name','birthday','team_long_name','team_short_name']).mean()
player_object = player_object.reset_index()
player_object''')
    st.markdown('This part of the code aggregates player attributes by player and team, calculating the mean of these attributes for each unique combination of player ID, name, birthday, and team name. This operation consolidates player stats across different matches or seasons into a single average value per player-team pairing, simplifying the dataset to one row per player-team combination, with their average stats.')
    st.code('''player_stats = pd.merge(player_object,category, on = ['player_api_id','player_name','birthday','team_long_name','team_short_name'],
                        how = 'left')''')
    st.markdown('Now we should merge the aggregated player attributes with another DataFrame category, which likely contains additional categorizations or information for players, based on their ID, name, birthday, and team name. The left join ensures all player-team pairs from the aggregated attributes are retained, enriching them with further category data.')
    st.code('''player_stats['attacking_work_rate'] = player_stats['attacking_work_rate'].replace({i:'None' for i in ['norm','stoc','le','y']})
player_stats['defensive_work_rate'] = player_stats['defensive_work_rate'].replace({i:'None' for i in ['_0','o','1','ormal','2','3','5','7','0','6','9','4','es','ean','tocky','8']})
player_stats''')
    st.markdown('''This code cleans up the attacking_work_rate and defensive_work_rate columns by replacing various non-standard or unclear values with 'None', standardizing the representation of these work rates across the dataset. This step improves the dataset's consistency, making these attributes more straightforward to analyze. Below is the first few rows of the final cleaned player_stats.''')
    st.markdown('This final code...')
    st.code('''player_stats['avg_defence_stats'] = player_stats[['standing_tackle','marking','sliding_tackle']].mean(axis = 1)''')
    st.code('''player_stats['defence_player'] = np.where(abs(player_stats['overall_rating'] - player_stats['avg_defence_stats']) <= 5,'Yes','No')''')
    st.dataframe(player_stats.head())

    st.subheader('Geojson Cleaning')
    st.markdown('In this case study, there will be frequent use of choropleth graphs to visualize data and help us draw useful conclusions. To do this, geojson files must be read in to create a map for the choropleth graphs to present. At the beginning, a self-customized geojson website was used to create a geojson file that only includes specific countries in Europe that will be beneficial for this case study. However, nearly all such websites consider the United Kingdom as a whole, while we require it to be separated, as the Scottish Premiership and the Premier League from England are considered separately. In this case, the data was gathered from Natural Earth<sup>1</sup>, and the binary files were downloaded through the internet and processed using ogr2ogr as follows:',unsafe_allow_html=True)
    st.code('''ogr2ogr sub_c.geojson ne_50m_admin_0_map_subunits
ls
ogr2ogr map_c.geojson ne_50m_admin_0_map_units''')
    st.markdown('This creates two seperate geojson files, one including the main file of Europe, with UK seperated into England and Scotland. The other one includes Belgium without being seperated into Flanders and Wallonia. The following code shows how to read in these net files to be used in the case study.')
    st.code('''world_path = mypath + 'map_c.geojson'
with open(world_path) as f:
    geo_world = json.load(f)
    
belgium_path = mypath + 'sovereign.geojson'
with open(belgium_path) as f:
    geo_belgium = json.load(f)''')
    st.markdown('''The code starts by setting up paths to two files: map_c.geojson and sovereign.geojson. These are special types of files used to store geographic data in a format called GeoJSON. The actual paths are formed by adding the file names to a variable mypath, which likely represents a directory on the computer where these files are stored. The code then opens the file map_c.geojson and reads its content. This file contains geographic data about Europe including information about various countries and their boundaries. Next, it opens the file sovereign.geojson and reads its content. This file contain detailed geographic data specifically about Belgium, such as its borders and regions.''')
    st.markdown('We then do the following code:')
    st.code('''map_country = team_info['country_name'].unique()
all_features = geo_world['features']

my_features = [feature for feature in all_features if feature['properties']['NAME'] in map_country]
belgium_feature = [feature for feature in geo_belgium['features'] if feature['properties']['NAME'] == 'Belgium']
my_features.append(belgium_feature)
geo_world['features'] = my_features''')


                
if selected=="Exploratory Analysis":
###Remember to add a short markdown before each graph to describe what it is about.

    st.title('Exploratory Analysis')
    st.subheader('Introduction to exploratary data analysis')
    st.markdown('''In this exploratory analysis, we examine the performance of football teams using box and scatter plots, explore geographical and hierarchical data with choropleth and sunburst graphs, and analyze detailed team metrics through histograms and advanced box plots. This approach offers insights into the characteristics of teams, their global distribution, and specific metrics, guiding us in a structured exploration of football data. You may manually select the variable you wish to explore.''')
    st.subheader('Overview and Performance Analysis')
    st.markdown('#### Graph 1: Box Plot')
    st.markdown('''This graph offers a comprehensive overview of each country's league level from multiple perspectives, including favorability and technical statistics. It aims to compare each league to identify relationships.''')
    col1,col2 = st.columns([4,5])
    with st.form('Select one category variable and one numeric variable'):
        #####Same issue here
        x_select = col1.selectbox('Select what category of teams you want to explore', np.setdiff1d(team_name_cols,'team_long_name'), key=1)
        y_select = col1.selectbox('Select what num information you want explore about the team', pretty_names_num.values(),key=2)
        y_select_df = [k for k,v in pretty_names_num.items() if v == y_select]
        coly_checkbox=col1.checkbox("check for log y-scale")
        submitted=st.form_submit_button("Submit to produce box plot")
        if submitted:
            log_y=False
            if coly_checkbox:
                log_y=True
            box = px.box(team_info,x=x_select,y=y_select_df[0],hover_name='team_long_name',color=x_select,log_y=log_y,labels=pretty_names_all,points='all',color_discrete_sequence = own_palette)
            col2.plotly_chart(box)
            
    st.markdown('#### Graph 2: Scatter Plot')
    st.markdown('This graph is to recognize if there is a correlation between two numeric stats using scatter plot.')
    col5,col6 = st.columns([4,5])
    with st.form('Select two numeric values to discover and a category variable for color'):
        x_select = col5.selectbox("Select what numeric value of teams do you want to explore",pretty_names_num.values(),key=5)
        x_select_df = [k for k,v in pretty_names_num.items() if v == x_select]
        y_select = col5.selectbox("Select what information you want to explore",[v for k,v in pretty_names_num.items() if k not in x_select_df],key=6)
        y_select_df = [k for k,v in pretty_names_num.items() if v == y_select]
        color_select = col5.selectbox("Select a grouping variable for colour",pretty_names_cat.values(),key=7)
        color_select_df = [k for k,v in pretty_names_cat.items() if v==color_select]
        colx_checkbox= col5.checkbox("Check for log x-scale")
        coly_checkbox= col5.checkbox("Check for log y-scale")
        submitted=st.form_submit_button("Submit to produce scatter plot")
        if submitted:
            log_x=False
            log_y=False
            if colx_checkbox:
                log_x=True
            if coly_checkbox:
                log_y=True
            scatter = px.scatter(team_info,x=x_select_df[0],y=y_select_df[0],hover_name='team_long_name',labels=pretty_names_all,color=color_select_df[0],log_x=log_x,log_y=log_y,color_discrete_sequence = own_palette)
            col6.plotly_chart(scatter)    
            
    st.subheader('Deep Dive into Team Metrics')
    st.markdown("#### Graph 1: Histogram")
    st.markdown('This graph demonstrates the relation of a numeric stat in correlation with a categorical stat.')
    col3,col4 = st.columns([4,5])
    with st.form("Select two category variable and one numeric variable"):
        x_select = col3.selectbox("Select what category of teams you want to explore",pretty_names_cat.values(),key=42434)
        x_select_df = [k for k,v in pretty_names_cat.items() if v == x_select]
        y_select = col3.selectbox("Select what numeric information of teams you want to explore",pretty_names_num.values(),key=32542)
        y_select_df = [k for k,v in pretty_names_num.items() if v == y_select]
        color_select = col3.selectbox('Select color for different teams in graph',pretty_names_cat.values(),key=8)
        color_select_df = [k for k,v in pretty_names_cat.items() if v == color_select]
        coly_checkbox=col3.checkbox("check for log y-scale",key=123523)
        submitted=st.form_submit_button("Submit to produce histogram")
        if submitted:
            log_y=False
            if coly_checkbox:
                log_y=True
            hist = px.histogram(team_info,x=x_select_df[0],y=y_select_df[0],log_y=log_y,color=color_select_df[0],width = 800, height = 800,labels=pretty_names_all,histfunc='avg',color_discrete_sequence = own_palette)
            col4.plotly_chart(hist)    
            
    st.markdown('#### Graph 2: Advanced Box Plot') 
    st.markdown('Different from the previous box plot, this graph shows the relation between one categorical technical data and a numeric stats.')
    col3,col4 = st.columns([4,5])
    with st.form('Select one team category variable and one numeric variable'):
        x_select = col3.selectbox('Select what category of teams you want to explore', [v for k,v in pretty_names_cat.items() if k not in team_name_cols], key=123)
        x_select_df = [k for k,v in pretty_names_cat.items() if v == x_select]
        y_select = col3.selectbox('Select what num information you want explore about the team', pretty_names_num.values(),key=321)
        y_select_df = [k for k,v in pretty_names_num.items() if v == y_select]
        coly_checkbox=col3.checkbox("check for log y-scale",key=12348)
        submitted=st.form_submit_button("Submit to produce box plot")
        if submitted:
            log_y=False
            if coly_checkbox:
                log_y=True      
            box = px.box(team_info,x=x_select_df[0],y=y_select_df[0],hover_name='team_long_name',labels=pretty_names_all,color=x_select_df[0],log_y=log_y,category_orders=category_order_dict,color_discrete_sequence = own_palette)
            col4.plotly_chart(box) 
            
    st.subheader('Geographic and Hierarchical Insights')  
    
    st.markdown('#### Graph 1: Choropleth Map') 
    st.markdown('This graph allows you to explore a numeric variable of each country and league, showing it as a form of map.')
    col9,col10 = st.columns([2,9])
    with st.form("Select variables to explore"):
        color_select = col9.selectbox("Numeric information",pretty_names_num.values(),key=325234)
        color_select_df = [k for k,v in pretty_names_num.items() if v == color_select]
        submitted=st.form_submit_button("Submit to produce choropeth")
        if submitted:
            chor = px.choropleth(team_info,locations = "country_name",color = color_select_df[0],height=950,width=950,labels=pretty_names_all,color_continuous_scale = px.colors.sequential.RdBu,color_discrete_sequence = own_palette,geojson=geo_world,featureidkey="properties.NAME",fitbounds = 'locations',basemap_visible = False,projection = 'natural earth')
            col10.plotly_chart(chor)
    
    st.markdown('#### Graph 2: Sunburst Graph')
    st.markdown('This graph allows you to explore a numeric value in terms of each league and each team seperately in the form of a sunburst graph.')
    col7,col8 = st.columns([4,5])
    with st.form("Select one numeric variable"):
        value_select = col7.selectbox("Select a numeric statistic you want to explore",pretty_names_num.values(),key=123283)
        value_select_df = [k for k,v in pretty_names_num.items() if v == value_select]
        submitted = st.form_submit_button('Submit to produce Sunburst')
        if submitted:
            sunburst_graph=px.sunburst(team_info.groupby(['league_name', 'country_name', 'team_long_name','favored_cutoff'])[num_cols].mean().reset_index(),path=['country_name','team_long_name'],labels=pretty_names_all,color='favored_cutoff',values=value_select_df[0],color_discrete_sequence = own_palette)
            #sunburst_graph=px.sunburst(team_info,path=['country_name','team_long_name'],labels=pretty_names_all,color='favored_cutoff',values=value_select_df[0])
            col8.plotly_chart(sunburst_graph)

if selected=="Analysis: Build Up Play":
    st.title('Analysis: Build Up Play')
    st.subheader('Passing')
    st.markdown('''Currently, it is believed that teams making shorter and more passes are better and more likely to win. This is because shorter passes are generally more accurate and easier to control, which helps a team maintain possession of the ball. Keeping possession can be a critical strategy in soccer, as it allows a team to dictate the pace of the game, conserve energy, and limit the opponent's opportunities to attack. Usually, only stronger teams with better players can make shorter passes and maintain control of the ball, as they possess the skills and techniques to make accurate passes that are less likely to be intercepted. On the other hand, weaker teams, to avoid interception by the opponent in dangerous areas, tend to clear the ball away through longer passes.''')
    st.markdown('''To visualize if the data agrees with our hypothesis, a box plot should be made. It would demonstrate the relationship between team favorability and build-up play passing. According to our hypothesis, the “Short” class should have the highest team favorability, followed by “Mixed,” and “Long” with the lowest. Below is the visualization of the box plot.''')
    passing_graph = px.box(team_all, x='buildUpPlayPassingClass',y='favored',color='buildUpPlayPassingClass',hover_name='team_long_name',labels=pretty_names_all,category_orders=category_order_dict)
    st.plotly_chart(passing_graph)
    st.markdown('''Through the plot, the general trend does follow the hypothesis. Short-passing teams have the highest position, followed by mixed and long passing. This conclusion aligns with existing research in soccer analytics. For example, a study by Hughes and Franks found that successful teams in international soccer tournaments made a higher percentage of short passes compared to less successful teams. This pattern was particularly evident in teams that progressed further in tournaments, emphasizing control over the ball and strategic build-up play. Another research by American Soccer Analysis suggests the relationship between pass completion rate and how often a team wins. The study also indicates that a high pass completion rate often correlates with short, safe passes, while a lower rate tends to involve riskier, longer passes.''')
    st.markdown('''However, there are two outliers that we should identify: Celtic and Inter Milan. Through research conducted, reasons why they are outliers have been found. For Inter Milan, a key aspect of their playing style that could explain their success as a long-passing team is the role of players like Marcelo Brozovic. During his time at Inter Milan, Brozovic completed the most passes in Serie A and made the most touches in the top-flight. His role as a metronome in possession, consistently making himself an option for the ball and finding the next pass, has been crucial to Inter Milan's style of play. This emphasis on skilled passers who can effectively control the game and dictate the pace through long passes could be a significant factor in why Inter Milan stands out as an effective long-passing team with high favorability. As for Celtic, under their manager Brendan Rodgers, they were well known for utilizing long passes as a strategy. Plus, they were significantly better than all the other teams in the Scottish leagues. That explains why, although they prefer long passing in build-up play, they are still highly favored.''')
    st.subheader('Speed')
    st.markdown('''Faster build-up play is often seen as a trade-off between risk and reward. While it can be risky, it also increases the chances of creating scoring opportunities due to numerical superiority in certain areas of the pitch. Coaches like Pep Guardiola and Gian Piero Gasperini invest significant time in training to improve players' functionality and automatism for executing fast build-up play effectively. Also, fast and coordinated build-up play can lead to quicker ball recovery when possession is lost. Guardiola’s approach at Barcelona involved moving forward together as a team, which minimized spaces and made it easier to regain possession.''') 
    st.markdown('''With top coaches such as Guardiola (often considered the most successful coach of the century) and strong teams all believing in the benefits of quick build-up play, it is fair to predict that faster build-up play speed is associated with a higher chance of winning, or being favored before a match.''')
    speed_graph = px.histogram(team_info,x='buildUpPlaySpeedClass',y='favored',color='country_name',width = 800, height = 800,labels=pretty_names_all,histfunc='avg',color_discrete_sequence = own_palette,category_orders=category_order_dict)
    st.plotly_chart(speed_graph)
    st.markdown('''The graph completely follows the hypothesis. I believe this is because fast build-up play aligns well with the high-tempo, high-pressing style of modern football. It allows teams to exploit spaces quickly, capitalize on opponents' disorganization, and create scoring opportunities before the opposition can settle into a defensive structure. Thus, teams with this playing style tend to be preferred by fans and analysts.''')
    st.markdown('''Another potential reason is that faster build-up play usually means a higher tempo of play for the team, thus making their gameplay more entertaining for spectators, contributing to their popularity. This results in attracting more fans and views, thus improving their favorability rating. This suggests that although the team might not actually be that good, they still receive a high favorability rating by its audience and fans favoring them over the other team. This indicates the idea of team favorability is a subjective decision by the betting audience reflecting the public and analysts' views.''')
    st.markdown('''As for balanced build-up play speed, it provides a middle ground. It is seen as a viable strategy, though not as preferred as fast build-up play. Balanced build-up offers a middle ground, maintaining some of the advantages of quick transitions while reducing risks associated with overly fast play. This approach might be favored by teams looking for a more controlled game while still exploiting opportunities to attack swiftly.''')
    st.markdown('''Finally, for slow build-up play, the lowest favorability for slow build-up play might reflect several perceptions. First, it is generally perceived as less effective: In the fast-paced nature of modern football, slow build-up play might be seen as less effective, especially against well-organized defenses. It might allow the opponent more time to set up their defensive structure, reducing the likelihood of finding gaps. Secondly, it's often the choice of teams that aren't good enough to execute faster strategies. The benefits of fast build-up play have already been outlined. Only teams that cannot accomplish this strategy due to technical issues choose this last option."''')

                

if selected=='Analysis: Chance Creation':
    st.title('Analysis: Chance Creation')
    st.subheader('Passing')
    hist = px.histogram(team_info,x='chanceCreationPassing',y='favored',width = 800, height = 800,labels=pretty_names_all,histfunc='avg',color_discrete_sequence = own_palette)
    st.markdown(' We present a histogram to analyze the relationship between chance creation through passing and team favorability. The notably high team favorability at the lowest chance creation passing score (20) is intriguing. This could indicate that certain teams, despite having a low rate of creating chances through passing, are still highly favored. This favorability could be attributed to several factors, such as these teams being very efficient in capitalizing on the few chances they create, or perhaps the sheer number of teams contributing to a high cumulative favorability rating.')
    st.markdown('The U-shaped distribution observed between scores of 30 and 70 suggests a non-linear relationship between chance creation through passing and team favorability. It might imply that teams with moderate chance creation passing scores (around the middle of the range) are not as favored. This could be due to the perception of these teams as average – not particularly strong in offense or defense. Fans and analysts might prefer teams that adopt either a very aggressive or very conservative play style, leading to higher favorability at these extremes.')
    st.markdown('''The stability in favorability for teams with chance creation passing scores between 75 and 80, which aligns with the average, indicates that teams with high chance creation ability are generally well-regarded but not exceptionally more than the average. This could suggest that high chance creation is expected from top teams, making it less of a distinguishing factor in their overall favorability. Additionally, fans and analysts might be considering other aspects of the team's play, such as defensive ability or style of play, in addition to their chance creation capabilities."''')
    st.plotly_chart(hist)
    st.subheader('Shooting')
    st.markdown('A common assumption is that a high volume of shots indicates a strong offensive team constantly attacking and creating scoring opportunities. The logic follows that more shots would lead to more goals, and therefore, a higher likelihood of winning matches. Teams with a "normal" level of shooting chances are often considered balanced, seen as creating a moderate number of opportunities but possibly focusing on the quality of shots rather than quantity. Teams with fewer shooting opportunities are often assumed to be more defensive or struggling offensively, with the hypothesis being that these teams might have lower win rates due to limited goal-scoring opportunities.')
    st.markdown("However, the analysis of the dataset and the visualization created show results that contradict these common assumptions regarding chance creation through shooting and a team's quality.")
    shooting_graph = px.box(team_all, x='chanceCreationShootingClass',y='favored',color='chanceCreationShootingClass',hover_name='team_long_name',labels=pretty_names_all,category_orders=category_order_dict)
    st.plotly_chart(shooting_graph)
    st.markdown('''Looking at the box plot, it's observed that although teams with "Lots" of chance creation shooting have the highest favorability rating, they are followed by those with "Little" instead of "Normal." This implies that teams with little chance creation shooting are actually better regarded than teams with normal chance creation shooting, indicating a misunderstanding of the classes.''')
    st.markdown('''For "Lots" of chance creation shooting, aligning with our hypothesis, it's fair to say that teams with a high volume of shots likely dominate offensively, maintaining consistent pressure on their opponents. This can lead to more scoring opportunities and, consequently, a higher chance of winning. Constant attacking and shooting can also exert psychological pressure on opponents, leading to defensive errors. In essence, taking more shots increases the probability of scoring goals. Teams that create a lot of shooting chances might convert enough of these into goals to win games, even if their overall shot conversion rate isn't exceptionally high.''')
    st.markdown('''Next, examining closely where the deviation occurs from what we might expect, a small amount of chance creation shooting could still result in a decent favorability rating. This might be because teams with fewer shooting opportunities may focus on counter-attacks or highly efficient, tactical play, waiting for high-quality chances rather than shooting frequently, leading to a higher conversion rate. Additionally, it's considered that teams shooting less often might invest more in defense, leading to fewer goals conceded and winning matches by narrow margins. They might prefer spending their resources on hiring a better manager who excels at defending and on acquiring defenders instead of attackers. Several graphs below are created to analyze this trend further. Lastly, teams with limited open-play shooting might excel in set-pieces, scoring from free kicks, corners, or penalties, compensating for fewer shots from open play.''')
    defence_hist = px.histogram(defence_info, x = 'chanceCreationShootingClass', y = 'avg_defence_stats',color='chanceCreationShootingClass', barmode='group', histfunc='avg')
    st.plotly_chart(defence_hist)
    defence_box = px.box(defence_info, x = 'chanceCreationShootingClass', y = 'avg_defence_stats',color='chanceCreationShootingClass', hover_name = 'team_long_name', hover_data = ['favored'],points='all',labels=pretty_names_all)
    defence_box.update_traces(
    hovertemplate=f"<b>{pretty_names_all['team_long_name']}</b>: %{{hovertext}}<br><br>" +
                  f"{pretty_names_all['avg_defence_stats']}: %{{y}}<br>" +
                  f"{pretty_names_all['favored']}: %{{customdata[0]}}" +
                  '<extra></extra>'
)
    st.plotly_chart(defence_box)    
    st.markdown(''''The above two graphs display the same trend: the average rating of defenders in little shooting teams is higher than in normal shooting teams. Although the difference is not incredibly large, it is sufficient for us to identify the underlying trend. This explains why, even though little shooting teams shoot less, they are still considered better. This could also be understood from the fans' perspective. An old saying goes, "attack wins you matches, defense wins you trophies," highlighting the importance of defense in the sport. This deeply ingrained mindset among the majority of fans might be the core reason why people tend to favor these little shooting teams more compared to normal shooting teams.''')
    
    
    
if selected=='Analysis: Defence':
    st.title('Defence')
    st.subheader('Pressure')
    st.markdown('''Defensive pressure is typically used to measure the intensity each team exerts on their opponents during gameplay. By analyzing leagues on a larger scale, we can reflect not only on each league's unique characteristics but also on the playing style and football philosophy of each country. Below is a choropleth graph that presents the defensive pressure of the highest division league in each country.''')
    chor = px.choropleth(team_info,locations = "country_name",color = 'defencePressure',height=950,width=950,labels=pretty_names_all,color_continuous_scale = px.colors.sequential.RdBu,color_discrete_sequence = own_palette,geojson=geo_world,featureidkey="properties.NAME",fitbounds = 'locations',basemap_visible = False,projection = 'natural earth')
    st.plotly_chart(chor)
    st.markdown('''After reviewing the visualization, we should focus on each league to determine which playing style is the most effective, thereby offering insights into the reasons behind some leagues' success and potentially linking to the characteristics that define a good team. We will start with Portugal. Portuguese teams might employ a more balanced approach to defense, with the lowest defense pressure at 39, focusing on positional play and tactical discipline rather than intense pressing. This approach could be influenced by the league's overall playing style, which traditionally favors technical skill and tactical organization. However, it's important to note that the Portuguese league is considered one of the weaker leagues, suggesting that a strategy focused solely on tactical discipline and recovery does not necessarily constitute a good team.''')
    st.markdown('''Next, we examine the top 5 leagues in the world: Spain, England, Germany, France, and Italy. Most of these leagues fall within the range of 45-59, except for the outlier of England. The Premier League is known for its fast-paced and physically demanding style of play. However, the impression of high pressure may be influenced by certain teams known for their intense pressing, such as those coached by Jurgen Klopp or Pep Guardiola. The overall league rating might be lower due to a mix of different playing styles among other teams, some of which might employ a more conservative or varied approach to defense. Thus, with the outlier explained, we understand that for top leagues, the average defensive pressure is moderate, without being too extreme, and this could serve as a reference for evaluating a team's favorability.''')
    st.markdown('''LLast but not least, Scotland should be analyzed with the highest defensive pressure. Scottish football has a long-standing tradition of physical, high-energy play. This often translates into a style of football where teams are more inclined to apply aggressive pressure, especially in defensive situations. The top teams, like Rangers and Celtic (especially Celtic), exhibit high defensive pressure, influencing the league's playing style. However, the highest defensive pressure does not necessarily translate to success. While still considered one of the big leagues in Europe, they have never been as successful as the other top leagues, indicating that extremely high defensive pressure is not as effective as a medium range, but still better than very low defensive pressure.''')
    st.subheader('Aggression')
    st.markdown(''''Besides defensive pressure, another key factor in evaluating a team's defense is their aggression. At first glance, defensive pressure and aggression might seem similar, yet a major difference exists. Defensive pressure is about the method and location on the pitch where a team applies effort to regain control of the ball, focusing more on the positional and strategic aspects of defense rather than on physical or aggressive nature. In contrast, defensive aggression pertains to how aggressively a team's defensive players act to regain possession of the ball. This could include the frequency and intensity of tackles, the willingness to physically challenge opponents, the tendency to intercept passes, and the likelihood of committing fouls as a result of aggressive play.''')
    sunburst_graph=px.sunburst(team_info.groupby(['league_name', 'country_name', 'team_long_name','favored_cutoff'])[num_cols].mean().reset_index(),path=['country_name','team_long_name'],labels=pretty_names_all,color='defencePressure',values='defenceAggression',color_discrete_sequence = own_palette)
    st.plotly_chart(sunburst_graph)
    st.markdown('''Through this sunburst graph, the size of each team is determined by the value of their defensive aggression. The larger their size within the circle, the higher their defensive aggression. This sunburst graph effectively shows the hierarchical relationship between countries, leagues, and teams. Despite the data's complexity (covering countries, leagues, and teams), this chart represents the information compactly and intuitively, allowing for easy comparison of defensive aggression across different levels. You can quickly identify which countries, leagues, or teams have higher or lower levels of aggression. However, when a league exhibits relatively average aggression, the visual impact might not be as pronounced.''')



if selected=="Conclusion":
    st.title("Conclusion")
    st.markdown("Through the final few analysis sections, we could identify the key statistics that a good team requires from each perspective, including build up play, chance creation, and defence, which covers the control, attack, and defence of the team. The multiple angle that we identify a good team means the research was explored through multiple lens. To briefly summarize, this case study identified the following characteristics in each of the fields of evaluation:")
    st.markdown('In build up play, teams with short passing length and quick build up play speed are favored the most. In chance creation, teams with lots of shooting opportunities are favored the most, followed by teams with little shooting opportunities. Teams with shooting opportunities in between is favored the least. Finally, in defence, leagues and teams with middle pressure and aggression are usually considered the best.')
    st.markdown('In the realm of build-up play, our research underscores the significance of adopting a strategy that prioritizes short passing lengths and swift transitions. This approach facilitates a fluid and dynamic game style, enabling teams to adapt quickly to on-field situations and outmaneuver opponents through agility and precision. It also underscores the fact that only strong teams have the ability to play in this style due to their technical players and manager. Fast build-up play is analyzed as a balance between risk and reward, with an emphasis on creating scoring opportunities through numerical superiority in attack phases. Fast build up play aligns with modern football, however could be costly if the opposing team gets a chance to counter attack. Balanced and slow build-up plays are considered less effective and favored, with slow play particularly perceived as a less viable option in contemporary football due to its ineffectiveness against organized defenses and its association with technically weaker teams.')
    st.markdown('''For chance creation, the evaluation had became much more complicated. For the first part on chance creation passing, it directly came down to an intriguing pattern where teams with the lowest chance creation passing score (20) are still highly favored, suggesting efficiency in capitalizing on limited opportunities might play a role in their favorability. A U-shaped distribution between scores of 30 and 70 indicates a non-linear relationship, where teams with moderate chance creation passing scores are less favored. However, teams with scores between 75 and 80, which align with the average, show stable favorability, suggesting that while high chance creation ability is valued, it might not be a standout factor in overall favorability as other aspects like defensive ability or style of play are also considered. The second part on chance creation shooting is also relatively complex. Contrary to common assumptions that more shots correlate with offensive strength and a higher likelihood of winning, the analysis reveals a different trend. While teams with "Lots" of chance creation shooting are the most favored, interestingly, teams with "Little" chance creation shooting are favored over those with a "Normal" level. The reasons behing was teams with little shooting actually had better defenders, and that was further supported by the graphs produced.''')
    st.markdown('''On the last part which is defence, the analysis focused on the defence agression and pressure. It begin with the analysis on defence pressure. The analysis starts by examining the defense pressure across various leagues using a choropleth graph, suggesting that it reflects each league's playing style and football philosophy. It examined the countries seperately and came to conclusion based on each country seperately. The section then differentiates between defense pressure and aggression, clarifying that while pressure is about strategic efforts to regain ball control, aggression focuses on the physical aspects of defense, such as tackling intensity and willingness to challenge opponents. A sunburst graph illustrates the hierarchical relationship between countries, leagues, and teams based on defense aggression, providing insights into how aggression varies across different tiers of soccer. The visualization indicates that while some teams or leagues might exhibit higher levels of aggression, the overall impact on success is nuanced and dependent on a balance of strategies.''')
    st.markdown('''In general, ''')
    
if selected=="Bibliography":
    st.title("Bibliography")
    st.markdown('[1] Connelly, Bill. “How Soccer Has Changed in the Past 10 Years: From Mourinho’s Peak to Reign of Superclubs.” ESPN.com, 19 Apr. 2020, www.espn.com/soccer/story/_/id/37582998/mourinho-peak-reign-super-clubs.')
    st.markdown('[2] Diacono, Tim. “One of the World’s Largest Sports Betting Agencies Is Set to Relocate to Malta.” Lovin Malta, 20 May 2018, lovinmalta.com/news/one-of-the-worlds-largest-sports-betting-agencies-is-set-to-relocate-to-malta/. Accessed 2 Mar. 2024.')
    st.markdown('[3] Natural Earth, https://www.naturalearthdata.com/')
    st.markdown('[4] ')



###BOX 1-league name + team favorability -- england most balanceddownloads/50m-cultural-vectors/50m-admin-0-details/, Date Accessed: 10 Jan 2024')


###BOX 2-Defence pressure + team favorability, chance creation passing + team favorability -- find outliers
###HIST 1-Country + Buildupplay speed, level of pace in each league.



#team_info.to_csv(mypath+'team_info.csv',index=False)












