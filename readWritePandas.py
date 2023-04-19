import pandas as pd

# Readint Two csv files as pandas dataframe and merge them based on User Id to get master dataframe
df = pd.merge(pd.read_csv("data1.csv") , pd.read_csv("data2.csv")[['uid','total_statements', 'total_reasons']], left_on='User ID',right_on = 'uid')
# Drom unnecessray columns
df.drop(['uid', 'S No'], axis=1, inplace=True)

# Removing Noise
# Convert Team Name --> LoWer Case
# Convert Lower case Team name --> Title Case
# Same goes for name
df['Team Name']= df['Team Name'].str.lower().str.title()
df['Name']= df['Name'].str.lower().str.title()

# **********************************************
# ******Teamwise Leaderboard Output Sheet*******
# **********************************************

# Getting List of all Team Names
teams = df['Team Name'].unique()

# Make dataframe with team leaderboard
teamLeaderBoard = pd.DataFrame(columns=['Thinking Teams Leaderboard', 'Average Statements', 'Average Reasons', 'total'])
loc = 0
for team in teams:
    dt = df.loc[df['Team Name'] == team]
    teamLeaderBoard.loc[loc] = [team, round(dt['total_statements'].mean(), 2), round(dt['total_reasons'].mean(), 2), round((dt['total_reasons'].mean() + dt['total_statements'].mean()), 2)]
    loc += 1

# Sorting based on the sum of avg
teamLeaderBoard.sort_values('total', ascending=False ,inplace=True)

# Drop Unnecessary columns
teamLeaderBoard.drop('total', axis=1, inplace=True)

# Reset the index after sorting
teamLeaderBoard.reset_index(inplace=True, drop=True)
teamLeaderBoard.index.name = 'Team Rank'

# Writing final output in csv file
teamLeaderBoard.to_csv('Leaderboard Teamwise.csv', index=True)

# ************************************************
# ******Individual Leaderboard Output Sheet*******
# ************************************************

# Extracting Dataframe with the useable fiels 
individualLeaderBoard = df.drop('Team Name', axis=1)

# Adding new column for sorting
individualLeaderBoard['total'] = individualLeaderBoard['total_statements'] + individualLeaderBoard['total_reasons']

# Sort the data based on the sum of two 
individualLeaderBoard.sort_values(['total', 'Name'], ascending=[False, True],inplace=True)

# Drop unnecessary columns
individualLeaderBoard.drop('total', axis=1, inplace=True)

# Reset the index after sorting 
individualLeaderBoard.reset_index(inplace=True, drop=True)
individualLeaderBoard.index.name = 'Rank'

# Rename the columns to get desired output
individualLeaderBoard.rename(columns={
    'User ID':'UID',
    'total_statements':'No. of Statements',
    'total_reasons':'No. of Reasons'
}, inplace=True)

# Writing the dataframe as csv file
individualLeaderBoard.to_csv('Leaderboard Individual.csv', index=True)