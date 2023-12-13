import sqlite3
import pandas as pd

# Connect to the databases
conn1 = sqlite3.connect('gamestats_database_c.db')
conn2 = sqlite3.connect('game_database_a.db')

# Read tables from both databases into two different dataframes
df1 = pd.read_sql_query("SELECT * FROM final_chart", conn1)
df2 = pd.read_sql_query("SELECT * FROM games2", conn2)

# Filter rows where abbreviation is 'LAL' in df2

df2 = df2[df2['home_team'].str.contains("'abbreviation': 'LAL'") | df2['visitor_team'].str.contains("'abbreviation': 'LAL'")]
# Modify your dataframes to use 'date' as index
df2.set_index('date', inplace=True)
df1.set_index('date', inplace=True)

# Merge dataframes based on 'date' index
merged_df = pd.merge(df2, df1, how='inner', on='date')

# Create new database from the merged dataframe
merged_db_connection = sqlite3.connect('merged_database.db')
merged_df.to_sql('MergedTable', merged_db_connection)

# Close all connections
conn1.close()
conn2.close()
merged_db_connection.close()

# Assuming that 'wins' and 'losses' columns exist in the merged_df DataFrame
 
# Create a scatterplot
sns.scatterplot(data=merged_df, x='date', y='wins', color='blue')
sns.scatterplot(data=merged_df, x='date', y='losses', color='red')

# Caculate and plot linear regression lines
slope, intercept, r_value_wins, p_value, std_err = stats.linregress(merged_df.index.values, merged_df['wins'])
slope2, intercept2, r_value_losses, p_value2, std_err2 = stats.linregress(merged_df.index.values, merged_df['losses'])

plt.plot(merged_df.index.values, slope * merged_df.index.values + intercept, color='blue')
plt.plot(merged_df.index.values, slope2 * merged_df.index.values + intercept2, color='red')

# print out the r-squared values
print("R-squared value for wins: ", r_value_wins ** 2)
print("R-squared value for losses: ", r_value_losses ** 2)

plt.show()