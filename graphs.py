import pandas as pd
from matplotlib import pyplot as plt

# Use functions from scraper
from scraper import (
    top_5_coins_prices,
    top_5_coins_market_caps,
    top_5_coins_24h_change,
    top_5_coins_7d_change
)

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
            print("Could not get market cap data")
            return

        # Clean and convert market cap data
        market_caps = []
        coin_names = []

        for _, row in top_coins.iterrows():
            market_cap_raw = str(row['Market Cap']).replace('$', '').replace(',', '')

            try:
                if market_cap_raw.endswith('B'):
                    value = float(market_cap_raw[:-1]) * 1_000_000_000
                elif market_cap_raw.endswith('M'):
                    value = float(market_cap_raw[:-1]) * 1_000_000
                elif market_cap_raw.endswith('K'):
                    value = float(market_cap_raw[:-1]) * 1_000
                else:
                    value = float(market_cap_raw)

                if value > 0:
                    market_caps.append(value)
                    coin_names.append(row['Coin'])

            except (ValueError, TypeError):
                print(f"Skipping {row['Coin']}: invalid market cap data")
                continue

        if not market_caps:
            print("No valid market cap data found")
            return

        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#4ECDC4']

        wedges, texts, autotexts = plt.pie(
            market_caps,
            labels=coin_names,
            autopct='%1.1f%%',
            colors=colors[:len(coin_names)],
            startangle=90,
            explode=[0.05] * len(coin_names)
        )

        plt.title('Market Cap Distribution - Top Cryptos', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.show()

        # Print summary
        print(f"\nPie chart created with {len(coin_names)} cryptocurrencies")
        for name, cap in zip(coin_names, market_caps):
            if cap >= 1_000_000_000:
                print(f"  {name}: ${cap / 1_000_000_000:.1f}B")
            elif cap >= 1_000_000:
                print(f"  {name}: ${cap / 1_000_000:.1f}M")
            else:
                print(f"  {name}: ${cap:,.0f}")

    except Exception as e:
        print(f"Error creating pie chart: {e}")

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
