from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import datetime

# Get current timestamp for data tracking
current_time = datetime.now()
timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Global variable to store the latest scraped data
latest_scraped_data = None


def scrape_data():
    """
    Scrapes cryptocurrency data from Coinlore website and returns it as a DataFrame.
    Includes current timestamp with each row of data.
    """
    global latest_scraped_data

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

    # Store the scraped data globally
    latest_scraped_data = df
    return df

def export_to_csv():
    """
    Exports the latest scraped cryptocurrency data to a CSV file.
    If file exists, appends new data; otherwise creates a new file.
    """
    global latest_scraped_data

    if latest_scraped_data is None:
        print("No data to export. Please scrape data first.")
        return


    file_path = r'C:\Users\mario\Desktop\PythonProject\crypto.csv'
    
    # Handle file operations based on whether file already exists
    if os.path.exists(file_path):
        # File exists - append new data without headers
        pd.read_csv(file_path)

        # Append new data to the existing CSV file
        latest_scraped_data.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Data appended to {file_path} with timestamp {timestamp}")
    else:
        # File doesn't exist - create new file with headers
        latest_scraped_data.to_csv(file_path, index=False)
        print(f"New file created at {file_path} with timestamp {timestamp}")


def read_csv_data(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    """
    Reads cryptocurrency data from a CSV file and returns it as a DataFrame.
    
    Args:
        file_path (str): Path to the CSV file. Defaults to the standard file path.
        
    Returns:
        pandas.DataFrame: DataFrame containing the cryptocurrency data.
        None: If the file doesn't exist or can't be read.
    """
    try:
        if os.path.exists(file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            return df
        else:
            print(f"File not found at {file_path}")
            return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def top_5_coins_prices(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    df = read_csv_data(file_path)
    temp_df = df.tail(10) #dataframe that consists only of the latest web scrape info
    return temp_df.head(5)[['Coin', 'Price']]

def top_5_coins_market_caps(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    df = read_csv_data(file_path)
    temp_df = df.tail(10)
    return temp_df.head(5)[['Coin', 'Market Cap']]

def top_5_coins_24h_change(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    df = read_csv_data(file_path)
    temp_df = df.tail(10)
    return temp_df.head(5)[['Coin', '24h']]

def top_5_coins_7d_change(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    df = read_csv_data(file_path)
    temp_df = df.tail(10)
    return temp_df.head(5)[['Coin', '7d']]

def get_coin_data_for_dropdown(file_path=r'C:\Users\mario\Desktop\PythonProject\crypto.csv'):
    """
    Returns coin names and IDs for dropdown menus with values.
    """
    df = read_csv_data(file_path)
    if df is not None:
        # Get latest data
        latest_timestamp = df['Timestamp'].max()
        latest_df = df[df['Timestamp'] == latest_timestamp]
        # Return dictionary with name as key and other data as needed
        return {row['Coin']: row['#'] for _, row in latest_df.iterrows()}
    return None