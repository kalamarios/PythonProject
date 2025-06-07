import random
import re

PATTERNS = {
    'greeting': {
        'keywords': [ 'hi', 'hello', 'good morning', 'good evening'],
        'responses': [
            'Hi! I am your personal cryptocurrency assistant. How can I help you?',
            'Hi! Go ahead and ask me anything you want about cryptocurrency',
            'Welcome! How can I help you with your questions about crypto?'
        ]

    },

    'crypto_basics': {
        'keywords':[ 'crypto' , 'bitcoin', 'explain', 'cryptocurrency', 'explain crypto' ],
        'responses': [ 'A cryptocurrency is a digital currency designed to work through a computer network ' ,
        'Cryptocurrency is not reliant on any central authority, such as a government or bank, to uphold or maintain it.'
        ]
    },

    'price_info': {
        'keywords': ['price', 'value', 'prices', 'money', 'currency', 'coin', 'current price', 'price now'],
        'responses': ['The prices of cryptocurrencies are constantly changing based on supply and demand in the markets.',
                      'You can see the current prices in our application. They are being updated in real time',
                      'The Prices are affected by many factors: news, regulations, adoption by companies, etc. ']

    },

    'price_changes': {
        'keywords': ['24 hours', '7 days', 'change','rise', 'fall','increase', 'decrease', 'change in 7 days', '24h change'],
        'responses':['The 24-hour change shows how much the price has changed in the last 24 hours in %. ', 
                    'The 7-day change shows the weekly trend - whether the currency is rising or falling.',
                    'Changes help us understand market trends. Green = up, red = down.' ]
    },

    'volume': {
        'keywords': ['volume', 'transactions', 'trading', 'trading volume'],
        'responses': ['Trading volume shows how much money changes hands in 24 hours for a crypto ',
                     'High volume means high interest and liquidity - easy to buy/sell.',
                       'Low volume may mean less interest or difficulty in trading.']
    },

    'advice': {
        'keywords': [ 'advice', 'what to do', 'beginner', 'beginner friendly', 'how to start', 'investment advice'],
        'responses': [ 'For beginners: Learn the basics first, do not invest money you can not afford to lose',
                      'Do your own research before investing.',
                      'Do not rely solely on tips.',
                      'Start with small amounts, learn how the markets work, and be prepared for prices changing'
        ]
    },

    'app_usage': {
        'keywords': ['app', 'how to use', 'data', 'graphs', 'application', 'how to', 'view graphs'],
        'responses' : ['In our app you can see prices, scrape new data, and view graphs!',
                       'Use the "Scraping" button for new data and select a currency from the list for charts.',
                       'The application saves data in CSV files that you can export and analyze.'
                       ]
    },

    'risks': {
        'keywords': ['risk', 'danger', 'fraud', 'safe', 'sure', 'risks'],
        'responses': [ 'Cryptocurrencies are very volatile - prices can change dramatically quickly,'
                        'Risks: volatility, government regulations, technical problems, fraud and hacking',
                        'Never invest more than you can afford to lose. The crypto market is quite risky!'
                    ]
    },

    'popular_crypto': {
        'keywords': ['better', 'popular', 'bitcoin', 'ethereum', 'what to choose', 'most popular crypto'],
        'responses': ['The most popular are Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB), Cardano (ADA)',
                      'Bitcoin is the first and most well-known, Ethereum allows smart contracts and DeFi applications',
                      'Popularity does not always mean a good investment. Do your own research!'

        ]
    }

}

# function to process user input
def process_input(user_input):
    """processes user input"""
    # Make letter lowercase
    processed = user_input.lower()
    
    # no punctuation marks 
    processed = re.sub(r'[^\w\s]', '', processed)
    
    # remove blank spaces
    processed = ' '.join(processed.split())
    
    return processed

#function to find matching patterns
def find_pattern(processed_input):
    """finds whcih pattern best fits with the input"""
    best_match = None
    max_matches = 0
    
    # split input into words
    input_words = processed_input.split()
    
    # check every pattern
    for pattern_name, pattern_data in PATTERNS.items():
        matches = 0
        
        # count how many keywords we found
        for keyword in pattern_data['keywords']:
            if keyword.lower() in processed_input:
                matches += 1
        
        # we choose the pattern with the most matches
        if matches > max_matches:
            max_matches = matches
            best_match = pattern_name
    
    return best_match if max_matches > 0 else None

#function for choosing the answer
def get_response(pattern):
    """ returns a random response for the given pattern"""
    if pattern and pattern in PATTERNS:
        responses = PATTERNS[pattern]['responses']
        return random.choice(responses)
    else:
        # responses for when the chatbot doesn't understand
        default_responses = [
        
            "I do not understand. Can you ask me something else?",
            "I am not sure about what you mean. Try asking me about cryptocurrency!",
            "Can you please rephrase your question?"
        ]
        return random.choice(default_responses)

#main function for chatbot 
def chatbot():
    """Main function for running the chatbot """
    print("🤖 Crypto Chatbot started!")
    print("Type 'exit' or 'quit' to terminate \n")
    
    while True:
        # input from the user 
        user_input = input("You : ").strip()
        
        # check for output
        if user_input.lower() in ['output', 'quit', 'exit', 'bye']:
            print("🤖 Bot: Bye! Glad to help you!")
            break
        
        # if user didn't write anything 
        if not user_input:
            print("🤖 Bot: Write something so that I can help you!")
            continue
        
        # process input
        processed = process_input(user_input)
        
        # find  matching pattern
        pattern = find_pattern(processed)
        
        # get and show response
        response = get_response(pattern)
        print(f"🤖 Bot: {response}\n")

if __name__ == "__main__":
    chatbot()



