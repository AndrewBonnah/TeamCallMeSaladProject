import sqlite3
import pandas as pd
import os
import sys
def initialize_database(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
 
    # Create a cursor object
    cur = conn.cursor()
 
    # Create table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS basketball_data (
        player_name TEXT,
        team_name TEXT,
        points INTEGER
    );
    ''' 

    # Execute the query
    cur.execute(create_table_query)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Call the function with your database file

def update_db(csv_file, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Extract table name from the CSV filename
    table_name = os.path.splitext(os.path.basename(csv_file))[0] 
    progress_table = 'progress'

    # Create table progress if it doesn't exist
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {progress_table} (
            table_name TEXT PRIMARY KEY, 
            last_row_processed INTEGER
        )
    ''')
    
    # Get the last processed row
    cur.execute(
        'SELECT last_row_processed FROM progress WHERE table_name = ?', 
        (table_name,)
    )
    result = cur.fetchone()
    
    if result:
        last_row_processed = result[0]
        
    else:
        last_row_processed = 0
        cur.execute(
            'INSERT INTO progress VALUES (?, ?)', 
            (table_name, last_row_processed)
        )
        

    # Read the next batch of rows
    batch_size = 25
    chunk = pd.read_csv(csv_file, skiprows=range(1, last_row_processed + 1), nrows=batch_size, header=0)

    # Only process if there are rows
    if not chunk.empty:
        # Write the data to a sqlite table
        chunk.to_sql(table_name, conn, if_exists='append', index=False)
        # Update the last processed row
        last_row_processed += len(chunk)
        cur.execute(
            'UPDATE progress SET last_row_processed=? WHERE table_name=?', 
            (last_row_processed, table_name)
        )
    else:
        sys.exit(1)
        exit
        return None

    # Commit after each chunk has been written
    conn.commit()

    # Close connection
    conn.close()
# Call function with your csv file and database file
# Call function with your csv file and database file


# Call the function with your csv file and database file
initialize_database('gamestats_database_c.db')
update_db('final_chart.csv', 'gamestats_database_c.db')