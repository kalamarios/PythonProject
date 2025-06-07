import pandas as pd
from matplotlib import pyplot as plt

# Use functions from scraper
from scraper import (
    read_csv_data,
    top_5_coins_prices,
    top_5_coins_market_caps,
    top_5_coins_24h_change,
    top_5_coins_7d_change
)

#load data from csv (keeping this for statistics function)
def load_crypto_data(csv_file='crypto.csv'):
    
    try:
        df = pd.read_csv(csv_file)
        df = df.tail(10).copy()
        
        # clean in price to just have the number
        df['Price_Clean'] = df['Price'].str.replace('$', '').str.replace(',', '')
        df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')
        
        # clean in mararketcap to just have the number
        df['MarketCap_Clean'] = df['Market Cap'].str.replace('$', '').str.replace(',', '')
        
        # convert billions, millions, thousands to actual numbers
        market_cap_values = []
        for value in df['MarketCap_Clean']:
            try:
                if 'B' in str(value):                   
                    market_cap_values.append(float(str(value).replace('B', '')) * 1_000_000_000)
                elif 'M' in str(value):                 
                    market_cap_values.append(float(str(value).replace('M', '')) * 1_000_000)
                elif 'K' in str(value):                  
                    market_cap_values.append(float(str(value).replace('K', '')) * 1_000)
                else:                                    
                    market_cap_values.append(float(str(value)))
            except:
                market_cap_values.append(0)             
        
        df['MarketCap_Clean'] = market_cap_values
        
        # in changes array delete the precentage
        df['Change_24h'] = pd.to_numeric(df['24h'].str.replace('%', ''), errors='coerce')
        df['Change_7d'] = pd.to_numeric(df['7d'].str.replace('%', ''), errors='coerce')
        
        print(f" Loaded {len(df)} cryptos")
        return df
        
    except Exception as e:
        print(f" Error while loading: {e}")
        return None

#bar chart for the 5 top prices
def show_barchart():
    
    try:
        # Get top 5 prices directly from scraper function
        top_coins = top_5_coins_prices()
        
        if top_coins is None or top_coins.empty:
            print("Could not get top 5 prices data")
            return
        
        # Clean the price data
        prices_clean = top_coins['Price'].str.replace('$', '').str.replace(',', '')
        prices_clean = pd.to_numeric(prices_clean, errors='coerce')
        
        plt.figure(figsize=(10, 6))
        plt.bar(top_coins['Coin'], prices_clean, color=['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#4ECDC4'])
        
        # Add price labels on bars
        for i, v in enumerate(prices_clean):
            plt.text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Top 5 Cryptos Prices', fontsize=14, fontweight='bold')
        plt.xlabel('Crypto')
        plt.ylabel('Price (USD)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error showing top prices: {e}")

#creation of market cap pie using the scraper funcctions


def show_market_cap_pie():
    try:
        # Get top 5 market cap data
        top_coins = top_5_coins_market_caps()

        if top_coins is None or top_coins.empty:
            print("Could not get top 5 market cap data")
            return

        print("Raw market cap data:")
        print(top_coins[['Coin', 'Market Cap']].head())

        # Lists to store only valid data
        valid_market_caps = []
        valid_coin_names = []

        # Process each coin and only keep valid ones
        for i, row in top_coins.iterrows():
            try:
                # Get the market cap value and handle it more carefully
                market_cap_raw = row.get('Market Cap', '')

                # Skip if empty or NaN
                if pd.isna(market_cap_raw) or market_cap_raw == '' or market_cap_raw == 'N/A':
                    print(f"Skipping {row.get('Coin', 'Unknown')}: No market cap data")
                    continue

                # Convert to string and clean it
                market_cap_str = str(market_cap_raw).strip()

                # Remove $ and commas
                market_cap_str = market_cap_str.replace('$', '').replace(',', '')

                # Initialize converted value
                converted_value = 0

                # Handle conversion with proper decimal support
                if market_cap_str.upper().endswith('B'):
                    # Remove 'B' and convert to float, then multiply by billion
                    number_part = market_cap_str[:-1].strip()
                    if number_part:  # Make sure we have something to convert
                        converted_value = float(number_part) * 1_000_000_000
                elif market_cap_str.upper().endswith('M'):
                    # Remove 'M' and convert to float, then multiply by million
                    number_part = market_cap_str[:-1].strip()
                    if number_part:
                        converted_value = float(number_part) * 1_000_000
                elif market_cap_str.upper().endswith('K'):
                    # Remove 'K' and convert to float, then multiply by thousand
                    number_part = market_cap_str[:-1].strip()
                    if number_part:
                        converted_value = float(number_part) * 1_000
                else:
                    # No suffix, try to convert directly to float
                    if market_cap_str:  # Make sure string is not empty
                        converted_value = float(market_cap_str)

                # Only add if value is positive and valid
                if converted_value > 0:
                    valid_market_caps.append(converted_value)
                    valid_coin_names.append(row['Coin'])
                    print(f"Successfully processed {row['Coin']}: '{market_cap_raw}' -> {converted_value:,.0f}")
                else:
                    print(f"Skipping {row.get('Coin', 'Unknown')}: Converted value is 0 or negative")

            except (ValueError, TypeError, KeyError, AttributeError) as e:
                print(
                    f"Warning: Could not process market cap for {row.get('Coin', 'Unknown')}: '{market_cap_raw}' - Error: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error processing {row.get('Coin', 'Unknown')}: {e}")
                continue

        # Check if we have any valid data to plot
        if len(valid_market_caps) == 0:
            print("No valid market cap data found for pie chart")
            print("\nTrying alternative approach - using price data instead...")

            # Fallback: try to use price data if market cap fails
            try:
                price_data = top_5_coins_prices()
                if price_data is not None and not price_data.empty:
                    for i, row in price_data.iterrows():
                        try:
                            price_str = str(row['Price']).replace('$', '').replace(',', '')
                            price_val = float(price_str)
                            if price_val > 0:
                                valid_market_caps.append(price_val)
                                valid_coin_names.append(f"{row['Coin']} (Price)")
                        except:
                            continue

                    if len(valid_market_caps) == 0:
                        print("No valid data available for chart")
                        return
                    else:
                        print(f"Using price data instead with {len(valid_market_caps)} coins")
            except:
                print("Could not create chart with alternative data")
                return

        print(f"\nCreating pie chart with {len(valid_coin_names)} coins")

        # Create the pie chart with only valid data
        plt.figure(figsize=(14, 10))
        colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#4ECDC4']

        # Create pie chart with better text positioning
        wedges, texts, autotexts = plt.pie(
            valid_market_caps,
            labels=None,  # Remove labels from pie chart to avoid overlap
            autopct='%1.1f%%',
            colors=colors[:len(valid_coin_names)],
            startangle=90,
            explode=[0.08] * len(valid_coin_names),  # Slightly more separation
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'},
            pctdistance=0.85,  # Move percentage text closer to center
            labeldistance=1.1  # Position for labels (not used since labels=None)
        )

        # Improve percentage text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

        plt.title('Market Cap Distribution - Top Cryptos',
                  fontsize=18, fontweight='bold', pad=30)
        plt.axis('equal')

        # Create a comprehensive legend with market cap values
        legend_labels = []
        for name, cap in zip(valid_coin_names, valid_market_caps):
            if cap >= 1_000_000_000:
                legend_labels.append(f"{name}: ${cap / 1_000_000_000:.1f}B")
            elif cap >= 1_000_000:
                legend_labels.append(f"{name}: ${cap / 1_000_000:.1f}M")
            elif cap >= 1_000:
                legend_labels.append(f"{name}: ${cap / 1_000:.1f}K")
            else:
                legend_labels.append(f"{name}: ${cap:,.0f}")

        # Position legend outside the plot area
        plt.legend(
            wedges,
            legend_labels,
            title="Cryptocurrencies & Market Cap",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=11,
            title_fontsize=12,
            frameon=True,
            fancybox=True,
            shadow=True
        )

        # Show the plot
        plt.show()

        # Print summary
        print(f"\nPie chart created successfully with {len(valid_coin_names)} coins:")
        for name, cap in zip(valid_coin_names, valid_market_caps):
            if cap >= 1_000_000_000:
                print(f"  {name}: ${cap / 1_000_000_000:.1f}B")
            elif cap >= 1_000_000:
                print(f"  {name}: ${cap / 1_000_000:.1f}M")
            elif cap >= 1_000:
                print(f"  {name}: ${cap / 1_000:.1f}K")
            else:
                print(f"  {name}: ${cap:,.0f}")

    except Exception as e:
        print(f"Error showing market cap pie chart: {e}")
        import traceback
        traceback.print_exc()


def show_lineplot():
    # in line chart show the price cnages in 24h and 7h for 5 top coins
    try:
        # Get change data directly from scraper functions
        changes_24h = top_5_coins_24h_change()
        changes_7d = top_5_coins_7d_change()
        
        if changes_24h is None or changes_7d is None:
            print("Could not get price change data")
            return
        
        # Clean the change data (remove % signs)
        change_24h_clean = pd.to_numeric(changes_24h['24h'].str.replace('%', ''), errors='coerce')
        change_7d_clean = pd.to_numeric(changes_7d['7d'].str.replace('%', ''), errors='coerce')
        
        plt.figure(figsize=(10, 6))
        
        # Plot 24h changes
        plt.plot(changes_24h['Coin'], change_24h_clean, 
                 marker='o', linewidth=2, label='24h change (%)', color='#FF6B35')
        
        # Plot 7d changes
        plt.plot(changes_7d['Coin'], change_7d_clean, 
                 marker='s', linewidth=2, label='7d change (%)', color='#4ECDC4')
        
        plt.title('Change of Cryptos Prices', fontsize=14, fontweight='bold')
        plt.xlabel('Crypto')
        plt.ylabel('Percentage of change (%)')
        plt.legend()
        
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)  # Line at 0%
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error showing price changes: {e}")


def show_statistics(df):
    print("\n" + "="*40)
    print("Statistics of my cryptos")
    print("="*40)
    
    print(f"Total cryptos: {len(df)}")
    print(f"Average price: ${df['Price_Clean'].mean():,.2f}")
    
    # Most expensive 
    max_price_idx = df['Price_Clean'].idxmax()
    print(f"Most expensive: {df.loc[max_price_idx, 'Coin']} (${df['Price_Clean'].max():,.2f})")
    
    # Cheapest crypto
    min_price_idx = df['Price_Clean'].idxmin()
    print(f"Cheapest: {df.loc[min_price_idx, 'Coin']} (${df['Price_Clean'].min():,.2f})")
    
    print(f"\nChanges:")
    print(f"   Average change in 24 hours: {df['Change_24h'].mean():.2f}%")
    print(f"   Average change in 7days: {df['Change_7d'].mean():.2f}%")
    
    print("="*40)
