import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
from scipy import stats
# Connect to the merged database
conn = sqlite3.connect('merged_database.db')

# Read the merged table into a DataFrame
df = pd.read_sql_query("SELECT * FROM MergedTable", conn)

# Create separate DataFrames for when Lakers are home/away team
df_lakers_home = df[df['home_team'].str.contains("'abbreviation': 'LAL'")]
df_lakers_away = df[df['visitor_team'].str.contains("'abbreviation': 'LAL'")]
# Create new 'score' column in both new DataFrames using .assign() to avoid 'SettingWithCopyWarning'
df_lakers_home = df_lakers_home.assign(score=df_lakers_home['home_team_score'])
df_lakers_away = df_lakers_away.assign(score=df_lakers_away['visitor_team_score'])

data_filters = [
    ('home', 'Win', df_lakers_home[df_lakers_home['result'] == 'W']),
    ('home', 'Loss', df_lakers_home[df_lakers_home['result'] == 'L']),
    ('away', 'Win', df_lakers_away[df_lakers_away['result'] == 'W']),
    ('away', 'Loss', df_lakers_away[df_lakers_away['result'] == 'L']),
]

# Calculate and print the R-squared values for each filtered dataset
for location, result, data in data_filters:
    if not data.empty:
        slope, intercept, r_value, p_value, std_err = stats.linregress(data['assists'], data['score'])
        print(f"R-squared for {location} games where result is '{result}': {r_value**2:.2f}")

plot_home = sns.lmplot(x='assists', y='score', hue='result', data=df_lakers_home, markers='o', palette={"W": "g", "L": "r"}, legend=False)
plot_away = sns.lmplot(x='assists', y='score', hue='result', data=df_lakers_away, markers='o', palette={"W": "g", "L": "r"}, legend=False)

plt.show()
