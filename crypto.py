from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.coinlore.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

titles = soup.find_all('th')
table_titles = [title.text.strip() for title in titles ]
table_titles = list(filter(None, table_titles))
if table_titles:
    table_titles = table_titles[:-7]

df = pd.DataFrame(columns = table_titles)


column_data = soup.find_all('tr')

for row in column_data[1:11]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    individual_row_data = list(filter(None, individual_row_data))
    if individual_row_data:
        individual_row_data = individual_row_data[:-1]
    length = len(df)
    df.loc[length] = individual_row_data

print(df)
df.to_csv(r'C:\Users\mario\Desktop\PythonProject\crypto.csv', index = False)




