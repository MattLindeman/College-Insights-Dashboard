import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

# Header - Welcome to the College Basketball Insights Dashboard
st.title('Welcome to the College Basketball Insights Dashboard!')
st.write('Dive into the world of college basketball with a comprehensive collection of data spanning the last 5 seasons. This interactive dashboard is designed to explore the statistical landscape of teams, conferences, and performance metrics that define college basketball. Discover trends, compare team performances, and explore correlations between key metrics and wins. From Offensive Efficiency to Strength of Schedule, this dashboard offers a unique perspective on what drives success in the dynamic realm of college hoops.')


# Load data
url = 'https://raw.githubusercontent.com/MattLindeman/STAT386-Project/main/CBBdata19-23.csv'
df = pd.read_csv(url)

# Sort unique team names and conference names alphabetically
teams_sorted = sorted(df['Team'].unique())
conferences_sorted = sorted(df['Conf'].unique())

# Filters section
st.title('Data Filtering')
st.write('Here you can view and filter the dataset used for this dashboard. The data can be filtered by team(s), conference(s), and/or year(s).')

# Filter by teams
selected_teams = st.multiselect('Select Teams', teams_sorted)

# Filter by conferences
selected_conferences = st.multiselect('Select Conferences', conferences_sorted)

# Filter by years
selected_years = st.multiselect('Select Years', df['Season'].unique())

# Apply filters to the data
filtered_df = df[
    (df['Team'].isin(selected_teams) if selected_teams else df['Team'].notnull()) &
    (df['Conf'].isin(selected_conferences) if selected_conferences else df['Conf'].notnull()) &
    (df['Season'].isin(selected_years) if selected_years else df['Season'].notnull())
]

# Display the filtered data or original data if no filters are selected
if filtered_df.empty:
    st.write(df)
else:
    st.write(filtered_df)
    
# Explanation for each abbreviation
abbreviations = {
    'Rk': 'Rank on the Barthag Scale',
    'Team': 'College Basketball Team',
    'Conf': 'College Basketball Conference',
    'G': 'Amount of Games Played',
    'Wins': 'Total Regular Season Wins',
    'Losses': 'Total Regular Season Losses',
    'AdjOE': 'Adjusted Offensive Efficiency (Points scored per 100 possessions, adjusted for opponent)',
    'AdjDE': 'Adjusted Defensive Efficiency (Points allowed per 100 possessions, adjusted for opponent)',
    'Barthag': 'Power Rating (Chance of beating average D-1 team)',
    'EFG%': 'Effective Field Goal Percentage (Adjusts field goal percentage to account for three\'s being worth more)',
    'EFGD%': 'Defensive Effective Field Goal Percentage',
    'TOR': 'Turnover Rate (Percent of offensive possessions that result in a turnover)',
    'TORD': 'Defensive Turnover Rate (Percent of defensive possessions that result in a turnover)',
    'ORB': 'Offensive Rebound Percentage (Percent of available offensive rebounds grabbed)',
    'DRB': 'Offensive Rebound Allowed Percentage (Percent of available offensive rebounds grabbed by opposition)',
    'FTR': 'Free Throw Rate (Ratio of free throw attempts to field goal attempts)',
    'FTRD': 'Defensive Free Throw Rate (Opponent ratio of free throw attempts to field goal attempts)',
    '2P%': 'Two Point Percentage (Percent of two point shots attempted that went in)',
    '2P%D': 'Defensive Two Point Percentage (Percent of two point shots allowed that went in)',
    '3P%': 'Three Point Percentage (Percent of three point shots attempted that went in)',
    '3P%D': 'Defensive Three Point Percentage (Percent of three point shots allowed that went in)',
    '3PR': 'Three Point Rate (Ratio of three point attempts to two point attempts)',
    '3PRD': 'Defensive Three Point Rate (Opponent ratio of three point attempts to two point attempts)',
    'Season': 'Year of Data',
    'Elite': 'Percentage of games an elite team would project to lose against this schedule',
    'SoS': 'Strength of Schedule (Average of opponent Barthags)'
}

# Create a collapsible expander for explanations
with st.expander("Click here for Abbreviation Explanations"):
    for abbreviation, explanation in abbreviations.items():
        st.write(f"**{abbreviation}:** {explanation}")
    
# Heatmap section
st.title('Correlation Heatmap')
st.write('This graph shows how each of the numeric variables are correlated with each other. A -1 indicates a strong, negative correlation between the variables, a 1 indicates a strong, positive correlation, and a 0 indicates that there is no correlation between the two variables. The graph is particularly useful in seeing which variables are most correlated with wins.')
    
# Select numerical columns to calculate correlation
selected_columns = ['AdjOE', 'AdjDE', 'EFG%', 'EFGD%', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD',
                    '2P%', '2P%D', '3P%', '3P%D', '3PR', '3PRD']
selected_data = df[['Wins'] + selected_columns]

# Calculate correlation matrix
correlation_matrix = selected_data.corr()

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')

# Save the figure to a BytesIO object
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Display saved image in Streamlit
st.image(buffer)

# Select columns for analysis (including 'SoS')
selected_columns = ['Wins', 'AdjOE', 'AdjDE', 'EFG%', 'EFGD%', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD',
                    '2P%', '2P%D', '3P%', '3P%D', '3PR', '3PRD', 'SoS']

# Streamlit app title and selection boxes
st.title('Interactive Regression Plot')
st.write('This interactive plot allows you to make a scatterplot with two numeric variables. It also provides a regression line to show how the average of the y-axis variable changes as the x-axis variable increases or decreases.')

# Allow user to select X-axis and Y-axis variables with default values
selected_x = st.selectbox('X-axis Variable', selected_columns, index=selected_columns.index('SoS'))
selected_y = st.selectbox('Y-axis Variable', selected_columns, index=selected_columns.index('Wins'))

# Create the regression plot based on user-selected variables
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x=selected_x, y=selected_y, scatter_kws={'color': 'skyblue'}, line_kws={'color': 'red'})
plt.title(f'{selected_y} vs {selected_x}')
plt.xlabel(selected_x)
plt.ylabel(selected_y)

# Display the plot in Streamlit
st.pyplot(plt)
        
# Streamlit app title and selection boxes
st.title('Top Teams with Most Wins')
st.write('This interactive plot allows you to view what teams have had the most wins. The default option displays all 5 seasons as a total, but individual seasons can be selected. There are also filters than can change how many teams are displayed and whether or not the wins should be weighted by strength of schedule. When weighting by strength of schedule win numbers will look slightly different than the regular totals. This is because a win against a difficult opponent will count for more than a win against an easier opponent.')

# Get unique teams and aggregate wins
team_wins = df.groupby('Team')['Wins'].sum().reset_index()

# Selection box for the number of seasons
selected_seasons = st.selectbox('Select Number of Seasons', ['All'] + list(df['Season'].unique()))

# Filter data based on selected seasons
if selected_seasons != 'All':
    df = df[df['Season'] == selected_seasons]

team_wins = df.groupby('Team')['Wins'].sum().reset_index()
team_wins_sorted = team_wins.sort_values(by='Wins', ascending=False)

# Slider to select number of top teams to display
num_top_teams = st.slider('Select Number of Top Teams to Display', min_value=1, max_value=50, value=10)

# Checkbox for weighted wins
weighted_wins = st.checkbox('Show Weighted Wins')

# Calculate and visualize based on checkbox selection
if weighted_wins:
    df['WeightedWins'] = df['Wins'] * df['SoS']
    weighted_team_wins = df.groupby('Team')['WeightedWins'].sum().reset_index()
    weighted_team_wins_sorted = weighted_team_wins.sort_values(by='WeightedWins', ascending=False)
    
    # Visualization - Bar plot for top teams with weighted wins
    plt.figure(figsize=(12, 10))
    sns.barplot(data=weighted_team_wins_sorted.head(num_top_teams), x='WeightedWins', y='Team', palette='rocket')
    plt.title(f'Top {num_top_teams} Teams with Most Weighted Wins')
    plt.xlabel('Weighted Wins')
    plt.ylabel('Team')
    st.pyplot(plt)
else:
    # Visualization - Bar plot for top teams with regular wins
    plt.figure(figsize=(12, 10))
    sns.barplot(data=team_wins_sorted.head(num_top_teams), x='Wins', y='Team', palette='viridis')
    plt.title(f'Top {num_top_teams} Teams with Most Wins')
    plt.xlabel('Total Wins')
    plt.ylabel('Team')
    st.pyplot(plt)
    
# Streamlit app title
st.title('Average Wins per Team by Conference')
st.write('This interactive plot allows you to see which conferences have averaged the most wins per team. The graph defaults to view all 5 seasons, but individual seasons can be selected.')

# Calculate total wins and number of unique teams per conference
conf_summary = df.groupby(['Conf', 'Season']).agg({'Wins': 'sum', 'Team': 'nunique'}).reset_index()

# Selection box for the number of seasons
selected_seasons = st.selectbox('Select Number of Seasons', ['All'] + sorted(df['Season'].unique()), key='season_select')

# Filter data based on selected seasons
if selected_seasons != 'All':
    df_filtered = conf_summary[conf_summary['Season'] == selected_seasons]
else:
    df_filtered = conf_summary

# Calculate total wins and number of unique teams per conference for filtered data
conf_summary_filtered = df_filtered.groupby('Conf').agg({'Wins': 'sum', 'Team': 'nunique'}).reset_index()
conf_summary_filtered.columns = ['Conf', 'TotalWins', 'NumTeams']

# Calculate average wins per team per season
if selected_seasons == 'All':
    conf_summary_filtered['AvgWinsPerTeamPerSeason'] = conf_summary_filtered['TotalWins'] / (conf_summary_filtered['NumTeams'] * df['Season'].nunique())
else:
    conf_summary_filtered['AvgWinsPerTeamPerSeason'] = conf_summary_filtered['TotalWins'] / conf_summary_filtered['NumTeams']

# Visualization - Bar plot for average wins per team per season by conference
plt.figure(figsize=(10, 10))
sns.barplot(data=conf_summary_filtered.sort_values(by='AvgWinsPerTeamPerSeason', ascending=False),
            x='AvgWinsPerTeamPerSeason', y='Conf', palette='twilight')  # Using 'twilight' color palette
plt.title('Average Wins per Team by Conference')
plt.xlabel('Average Wins per Team')
plt.ylabel('Conference')
st.pyplot(plt)

# Streamlit app title
st.title('AdjOE and AdjDE for Selected Conferences')
st.write('This interactive plot allows you to see the AdjOE and AdjDE boxplots for teams within, what is often referred to as, power 6 conferences. There is also the option to add or remove any conferences of your choosing.')

# Default selection of top six conferences
default_conferences = ['B12', 'B10', 'SEC', 'ACC', 'P12', 'BE']

# Selection box for conferences
selected_conferences = st.multiselect('Select Conferences', df['Conf'].unique(), default=default_conferences)

# Filter dataset for selected conferences
selected_conferences_data = df[df['Conf'].isin(selected_conferences)]

# Visualization - Box plot for AdjOE and AdjDE for the selected conferences
plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
sns.boxplot(data=selected_conferences_data, x='Conf', y='AdjOE', order=selected_conferences, palette='pastel')
plt.title('AdjOE for Selected Conferences')
plt.xlabel('Conference')
plt.ylabel('AdjOE')

plt.subplot(1, 2, 2)
sns.boxplot(data=selected_conferences_data, x='Conf', y='AdjDE', order=selected_conferences, palette='pastel')
plt.title('AdjDE for Selected Conferences')
plt.xlabel('Conference')
plt.ylabel('AdjDE')

# Invert y-axis for AdjDE plot
plt.gca().invert_yaxis()

plt.tight_layout()
st.pyplot(plt)

# Streamlit app title
st.title('Offensive vs Defensive Efficiency')
st.write('This final graph compares the average wins for teams that were either in the top 10% for AdjOE or the top 10% for AdjDE. This provides a way to compare if offensive efficiency or defensive efficieny is more important for wins.')

# Calculate the threshold values for the top 10% in AdjOE and bottom 10% in AdjDE
top_10_AdjOE = df['AdjOE'].quantile(0.9)
bottom_10_AdjDE = df['AdjDE'].quantile(0.1)

# Filter dataset for top 10% in AdjOE and bottom 10% in AdjDE
top_10_AdjOE_data = df[df['AdjOE'] >= top_10_AdjOE]
bottom_10_AdjDE_data = df[df['AdjDE'] <= bottom_10_AdjDE]

# Exclude teams that are in the top 10% for AdjOE and bottom 10% for AdjDE
exclude_both = pd.merge(top_10_AdjOE_data, bottom_10_AdjDE_data, how='inner', on='Team')['Team']
filtered_AdjOE_data = top_10_AdjOE_data[~top_10_AdjOE_data['Team'].isin(exclude_both)]
filtered_AdjDE_data = bottom_10_AdjDE_data[~bottom_10_AdjDE_data['Team'].isin(exclude_both)]

# Calculate average wins for top 10% in AdjOE and bottom 10% in AdjDE excluding the intersection
avg_wins_top_AdjOE = filtered_AdjOE_data['Wins'].mean()
avg_wins_bottom_AdjDE = filtered_AdjDE_data['Wins'].mean()

# Create a combined DataFrame for boxplot
filtered_data = pd.concat([filtered_AdjOE_data['Wins'].rename('Top 10% AdjOE'), filtered_AdjDE_data['Wins'].rename('Top 10% AdjDE')], axis=1)

# Melt the DataFrame to prepare for boxplot
melted_data = pd.melt(filtered_data, var_name='Category', value_name='Average Wins')

# Create the boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(x='Category', y='Average Wins', data=melted_data, palette='pastel')
plt.title('Average Wins per Season for Top 10% AdjOE vs Top 10% AdjDE (Excluding Intersection)')
plt.ylabel('Average Wins')
plt.xticks([0, 1], ['Top 10% AdjOE', 'Top 10% AdjDE'])
plt.xlabel('Teams')

# Display the plot in Streamlit
st.pyplot(plt)

# Closing statement
st.write('I hope you enjoyed this dashboard and learned something new about college basketball!')

# Footer - Data Source Information
st.markdown('---')
st.write('The data for this dashboard was compiled through the [Barttorvik](https://barttorvik.com/#) college basketball analytics website. The code and process for collecting, cleaning, and exploring the data can be found here:')
st.write('Code: [GitHub](https://github.com/MattLindeman/STAT386-Project)')
st.write('Process: [Blog](https://mattlindeman.github.io)')
