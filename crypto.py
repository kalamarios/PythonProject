from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime

current_time = datetime.now()
timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

def scrape_data():

    url = 'https://www.coinlore.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    titles = soup.find_all('th')
    table_titles = [title.text.strip() for title in titles]
    table_titles = list(filter(None, table_titles))
    if table_titles:
        table_titles = table_titles[:-7]
    
    # Add timestamp column to the table titles
    table_titles.append('Timestamp')

    df = pd.DataFrame(columns=table_titles)

    column_data = soup.find_all('tr')

    for row in column_data[1:11]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        individual_row_data = list(filter(None, individual_row_data))
        if individual_row_data:
            individual_row_data = individual_row_data[:-1]
        
        # Add timestamp to each row
        individual_row_data.append(timestamp)
        
        length = len(df)
        df.loc[length] = individual_row_data

    return df

def export_to_csv():

    df = scrape_data()
    file_path = r'C:\Users\mario\Desktop\PythonProject\crypto.csv'
    
    # Check if file exists to decide whether to append or create new
    if os.path.exists(file_path):
        # Read existing data to ensure consistent column ordering
        existing_df = pd.read_csv(file_path) #existing_df not used for now

        # Append new data to the existing CSV file
        df.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Data appended to {file_path} with timestamp {timestamp}")
    else:
        # Create a new CSV file if it doesn't exist
        df.to_csv(file_path, index=False)
        print(f"New file created at {file_path} with timestamp {timestamp}")


export_to_csv()