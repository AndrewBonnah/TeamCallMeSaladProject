import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
url = "https://www.espn.com/nba/stats/player/_/season/2023/seasontype/2?limit=1000"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Make a GET request to the URL with headers
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table body
    table_body = soup.select_one('#fittPageContainer > div:nth-child(3) > div > div > section > div > div:nth-child(3) > div > div > div > div.Table__Scroller > table > tbody')

    # Define anchor_links outside of the if block
    anchor_links = soup.find_all('a', class_='AnchorLink')

    if table_body:
        # Find all rows in the table
        rows = table_body.find_all('tr')

        # Find all columns dynamically by inspecting the first row
        header_row = rows[0]
        columns = header_row.find_all('td')

        # Create lists to store all player details
        all_player_details = []

        # Iterate through each row and extract all player details
        for i, row in enumerate(rows):
            # Find player name
            player_name = anchor_links[i + 25].text.strip()  # Skip the first three elements (headers)

            # Find PTS value (adjust column index if needed)
            pts = float(row.select_one('td:nth-child(4)').text.strip())  # Convert to float

            # Append all player details to the list
            player_details = {
                'PlayerName': player_name,
                'PTS': pts,
                # Add more columns as needed
            }
            all_player_details.append(player_details)

            # Print all player name and values from all columns
            row_values = [player_name] + [cell.text.strip() for cell in row.find_all('td')]
            #print("\t".join(row_values))



# Create SQLite database and table
conn = sqlite3.connect('basketball_data.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS basketball_data (
                    PlayerName TEXT,
                    PTS REAL
                    -- Add more columns as needed
                 );''')

# Calculate the number of iterations needed to transfer all data in batches of 25
iterations = len(all_player_details) // 25 + (len(all_player_details) % 25 > 0)

# Iterate through the data and insert 25 records at a time
for i in range(iterations):
    start_index = i * 25
    end_index = start_index + 25
    batch_data = all_player_details[start_index:end_index]

    # Insert data into the table
    for player in batch_data:
        cursor.execute("INSERT INTO basketball_data VALUES (?, ?)", (player['PlayerName'], player['PTS']))

    # Commit changes after each batch
    conn.commit()

# Close connection
conn.close()

# Select top 25 players for plotting the graph
conn = sqlite3.connect('basketball_data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM basketball_data LIMIT 25")
top_25_data = cursor.fetchall()
conn.close()

# Connect to the SQLite database
conn = sqlite3.connect('basketball_data.db')

# Read the table into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM basketball_data", conn)

# Save the DataFrame to a CSV file
df.to_csv('player_data_y.csv', index=False)

# Close the database connection
conn.close()



# Select top 25 players for plotting the graph
top_25_player_names = [player['PlayerName'] for player in all_player_details][:25]
top_25_pts_values = [player['PTS'] for player in all_player_details][:25]

        # Plotting the graph for top 25 players with most points
plt.figure(figsize=(10, 6))
plt.bar(top_25_player_names, top_25_pts_values, color='hotpink')
plt.xlabel('Player')
plt.ylabel('Points (PTS)')
plt.title('Top 25 Players with Most Points')
plt.xticks(rotation=45, ha='right')  # Rotate player names for better visibility
plt.tight_layout()
plt.show()


