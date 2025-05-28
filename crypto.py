from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime

# Get current timestamp for data tracking
current_time = datetime.now()
timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

def scrape_data():
    """
    Scrapes cryptocurrency data from Coinlore website and returns it as a DataFrame.
    Includes current timestamp with each row of data.
    """
    # Target URL for cryptocurrency data
    url = 'https://www.coinlore.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extract table headers (column names)
    titles = soup.find_all('th')
    table_titles = [title.text.strip() for title in titles]
    table_titles = list(filter(None, table_titles))  # Remove empty strings
    if table_titles:
        table_titles = table_titles[:-7]  # Remove unnecessary columns
    
    # Add timestamp column to track when data was collected
    table_titles.append('Timestamp')

    # Create empty DataFrame with extracted column names
    df = pd.DataFrame(columns=table_titles)

    # Extract data from each row in the table
    column_data = soup.find_all('tr')

    # Process only first 10 cryptocurrencies (rows 1-10)
    for row in column_data[1:11]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        individual_row_data = list(filter(None, individual_row_data))  # Remove empty strings
        if individual_row_data:
            individual_row_data = individual_row_data[:-1]  # Remove last column
        
        # Add current timestamp to each row for tracking
        individual_row_data.append(timestamp)
        
        # Add the row to our DataFrame
        length = len(df)
        df.loc[length] = individual_row_data

    return df

def export_to_csv():
    """
    Exports scraped cryptocurrency data to a CSV file.
    If file exists, appends new data; otherwise creates a new file.
    """
    # Get cryptocurrency data
    df = scrape_data()
    file_path = r'C:\Users\mario\Desktop\PythonProject\crypto.csv'
    
    # Handle file operations based on whether file already exists
    if os.path.exists(file_path):
        # File exists - append new data without headers
        pd.read_csv(file_path)

        # Append new data to the existing CSV file
        df.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Data appended to {file_path} with timestamp {timestamp}")
    else:
        # File doesn't exist - create new file with headers
        df.to_csv(file_path, index=False)
        print(f"New file created at {file_path} with timestamp {timestamp}")


export_to_csv()