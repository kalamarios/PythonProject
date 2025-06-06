import pandas as pd
import matplotlib.pyplot as plt

# create data for trial
def create_sample_data():
    data = {
        'name': ['Bitcoin', 'Ethereum', 'Binance Coin', 'Cardano', 'Solana', 
                'XRP', 'Polkadot', 'Dogecoin', 'Avalanche', 'Chainlink'],
        'price_in_usd': [45000, 3200, 420, 1.25, 96, 0.65, 25, 0.08, 86, 15],
        'change_in_24h': [2.5, -1.8, 3.2, 5.1, -2.3, 1.7, -0.5, 8.9, 4.2, -3.1],
        'change_in_7d': [12.3, -5.2, 8.7, 15.6, -8.9, 3.4, -2.1, 25.8, 11.2, -6.7],
        'market_cap': [850000000000, 380000000000, 65000000000, 40000000000, 35000000000,
                      32000000000, 28000000000, 10000000000, 25000000000, 8000000000]
    }
    return pd.DataFrame(data)

# 1. Bar Chart for the prices of top 5 cryptocurrencies
def create_bar_chart(df):
    
    # 5 most expensive 
    top_5 = df.nlargest(5, 'price_in_usd')
    
    # Δcreate the graph
    plt.figure(figsize=(10, 6))
    plt.bar(top_5['name'], top_5['price_in_usd'], color='orange')
    
    # add titles
    plt.title('ΤPrices for the 5 cryptocurrencies')
    plt.xlabel('cryptocurrency')
    plt.ylabel('price (USD)')
    
    # rotate names
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # save and show
    plt.savefig('bar_chart.png')
    plt.show()

# 2. Pie Chart for capitalization
def create_pie_chart(df):
    
    # 5 top capitalized
    top_5 = df.nlargest(5, 'market_cap')
    
    # create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(top_5['market_cap'], labels=top_5['name'], autopct='%1.1f%%')
    
    plt.title('Distribution of Top 5 capitalised cryptos')
    
    # save and show
    plt.savefig('pie_chart.png')
    plt.show()

# 3. Line Plot for price change
def create_line_plot(df):
    
    # top 5 capitalised
    top_5 = df.nlargest(5, 'market_cap')
    
    # create line plot 
    plt.figure(figsize=(12, 6))
    
    # create 2 lines: one for 24h, one for 7d
    plt.plot(top_5['name'], top_5['change_in_24h'], marker='o', label='Change in 24h')
    plt.plot(top_5['name'], top_5['change_in_7d'], marker='s', label='Change in 7d')
    
    # add titles and labels
    plt.title('Price changes of top 5 cryptos')
    plt.xlabel('cryptos')
    plt.ylabel('Change percentage (%)')
    
    plt.legend()
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # save and show
    plt.savefig('line_plot.png')
    plt.show()

# Basic statistics
def print_statistics(df):
    print("=== CRYPTO STATISTICS ===")
    print(f"Total number : {len(df)}")
    print(f"Average : ${df['price_in_usd'].mean():.2f}")
    print(f"Most expensive: {df.loc[df['price_in_usd'].idxmax(), 'name']} (${df['price_in_usd'].max():.2f})")
    print(f"Cheapest: {df.loc[df['price_in_usd'].idxmin(), 'name']} (${df['price_in_usd'].min():.2f})")
    print(f"Average change in 24h: {df['change_in_24h'].mean():.2f}%")

# Main function
def main():
    
    print("Create data...")
    df = create_sample_data()
    
    print("Print statistics...")
    print_statistics(df)
    
    print("\nCreating graphs...")
    
    print("1. Bar Chart for prices ...")
    create_bar_chart(df)
    
    print("2. Pie Chart for capitalization...")
    create_pie_chart(df)
    
    print("3. Line Plot for change...")
    create_line_plot(df)
    
    print("End of program. The graphs have been saved as PNG files ")

if __name__ == "__main__":
    main()