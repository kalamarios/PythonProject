import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from scraper import (
    scrape_data,
    export_to_csv,
    read_csv_data,
    get_coin_data_for_dropdown,

)

from graphs import (
show_market_cap_pie,
show_barchart,
show_lineplot
)

# create gui for chatbot with imports
from chatbot import process_input, find_pattern, get_response

class CryptocurrencyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot - Specialist in cryptos")
        self.root.geometry("1400x900")
        self.root.configure(bg='light yellow')

        # Initialize data
        self.current_data = None
        self.selected_coin = tk.StringVar()

        self.create_widgets() #main window
        self.load_existing_data() #to load data that already exist

    def create_widgets(self):

        # Title
        title_label = tk.Label(
            self.root,
            text="Cryptos Data and Bot",
            font=("Times New Roman", 18, "bold"),
            bg='light yellow',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)


        main_container = tk.Frame(self.root, bg='light yellow')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Creating tabs so the user can choose what he prefers to use
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)


        self.data_tab = tk.Frame(self.notebook, bg='light yellow')
        self.notebook.add(self.data_tab, text="Cryptos Data")

        self.chat_tab = tk.Frame(self.notebook, bg='light yellow')
        self.notebook.add(self.chat_tab, text="Cryptos Bot")

        # Setting up tabs
        self.setup_data_tab()
        self.setup_chat_tab()

        # To show status with each command
        self.status_bar = tk.Label(
            self.root,
            text="Ready! Load data if you want to proceed",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#bdc3c7',
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_data_tab(self):
        # Main frame for data analysis
        main_frame = tk.Frame(self.data_tab, bg='light yellow')
        main_frame.pack(fill=tk.BOTH, expand=True)

        #create a panel on the left to handle all the controls using buttons
        left_panel = tk.Frame(main_frame, bg='light yellow', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Column for all the controls
        control_frame = tk.LabelFrame(left_panel, text="What do you want to do with the data", font=("Arial", 12, "bold"), bg='light yellow')
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # button to scrape new data
        self.scrape_btn = tk.Button(
            control_frame,
            text="Scrape new data",
            command=self.scrape_new_data,
            bg='pink',
            fg='white',
            font=("Times New Roman", 10, "bold"),
            pady=5
        )
        self.scrape_btn.pack(fill=tk.X, padx=5, pady=5)

        # button to export the data that was scrasped to the CSV file
        self.export_btn = tk.Button(
            control_frame,
            text="Export to  CSV",
            command=self.export_data,
            bg='violet',
            fg='white',
            font=("Times New Roman", 10, "bold"),
            pady=5
        )
        self.export_btn.pack(fill=tk.X, padx=5, pady=5)

        # dropdown frame to choose ctypto
        selection_frame = tk.LabelFrame(left_panel, text="Choose Crypto", font=("Times New Roman", 12, "bold"), bg='magenta')
        selection_frame.pack(fill=tk.X, padx=10, pady=10)

        # Dropdown for coin selection
        tk.Label(selection_frame, text="Choose Crypto:", bg='light yellow', font=("Times New Roman", 10)).pack(pady=5)

        self.coin_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_coin,
            state="readonly",
            font=("Times New Roman ", 10)
        )
        self.coin_dropdown.pack(fill=tk.X, padx=5, pady=5)
        self.coin_dropdown.bind('<<ComboboxSelected>>', self.on_coin_selected)

        # Add "Show All" button
        self.show_all_btn = tk.Button(
            selection_frame,
            text="Show all",
            command=self.show_all_coins,
            bg='#34495e',
            fg='white',
            font=("Arial", 9),
            pady=3
        )
        self.show_all_btn.pack(fill=tk.X, padx=5, pady=5)

        # Charts section
        charts_frame = tk.LabelFrame(left_panel, text="Graphs of Data", font=("Arial", 12, "bold"), bg='light blue') #main frame gia kouti
        charts_frame.pack(fill=tk.X, padx=10, pady=10)

        # buttons that are included in the main frame for the graphs
        self.bar_chart_btn = tk.Button(
            charts_frame,
            text="Bar Chart - Calculating Top 5 Prices",
            command=self.show_bar_chart,
            bg='light pink',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.bar_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        self.pie_chart_btn = tk.Button(
            charts_frame,
            text="🥧 Pie Chart - Calculating the Market Cap",
            command=self.show_pie_chart,
            bg='light pink',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.pie_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        self.line_chart_btn = tk.Button(
            charts_frame,
            text=" Line Plot - 24h / 7d",
            command=self.show_line_chart,
            bg='light pink',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.line_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        # Right panel for data display
        right_panel = tk.Frame(main_frame, bg='light yellow')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Data table section
        table_frame = tk.LabelFrame(right_panel, text="Datas of Cryptos", font=("Arial", 12, "bold"),
                                    bg='light yellow')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Treeview for data display
        self.create_data_table(table_frame)

    def setup_chat_tab(self):
        """Setup the chatbot tab"""
        # Main chat frame
        chat_main_frame = tk.Frame(self.chat_tab, bg='light yellow')
        chat_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Chat title
        chat_title = tk.Label(
            chat_main_frame,
            text=" Bot ",
            font=("Times New Roman ", 16, "bold"),
            bg='light yellow',
            fg='#2c3e50'
        )
        chat_title.pack(pady=(0, 20))

        # Chat display area
        chat_display_frame = tk.LabelFrame(
            chat_main_frame, 
            text="Ask me!",
            font=("Arial", 12, "bold"),
            bg='light pink'
        )
        chat_display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_display_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 11),
            bg='light pink',
            fg='#2c3e50',
            state=tk.DISABLED,
            relief=tk.GROOVE,
            bd=2
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input frame
        input_frame = tk.Frame(chat_main_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Input label
        input_label = tk.Label(
            input_frame,
            text="Ask me anything about cryptocurrency:",
            font=("Arial", 12, "bold"),
            bg='violet',
            fg='#34495e'
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))

        # entry frame
        entry_frame = tk.Frame(input_frame, bg='light yellow')
        entry_frame.pack(fill=tk.X)

        # Chat input -> entry frame kid
        self.chat_input = tk.Entry(
            entry_frame,
            font=("Arial", 12),
            relief=tk.GROOVE,
            bd=2
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Send button
        self.send_btn = tk.Button(
            entry_frame,
            text="Send ->",
            command=self.send_message,
            bg='light blue',
            fg='white',
            font=("Arial", 11, "bold"),
            pady=5,
            padx=15,
            relief=tk.RAISED,
            bd=2
        )
        self.send_btn.pack(side=tk.RIGHT)

        # Bind Enter key to send message
        self.chat_input.bind('<Return>', lambda event: self.send_message())

        # Control buttons frame
        control_buttons_frame = tk.Frame(chat_main_frame, bg='#f0f0f0')
        control_buttons_frame.pack(fill=tk.X)

        # button for clearing chat
        self.clear_chat_btn = tk.Button(
            control_buttons_frame,
            text=" Clear Chat",
            command=self.clear_chat,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10),
            pady=3,
            padx=10
        )
        self.clear_chat_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Quick questions frame
        quick_frame = tk.LabelFrame(
            chat_main_frame,
            text="Quick Questions",
            font=("Arial", 11, "bold"),
            bg='#f0f0f0'
        )
        quick_frame.pack(fill=tk.X, pady=(10, 0))



        # Add welcome message
        self.add_chat_message("🤖 Bot",
                             "Hi! I'm your cryptocurrency assistant. Ask me anything about crypto, prices, investment advice, or how to use this application!")

    def add_chat_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Format message
        if sender == "You":
            formatted_message = f"[{timestamp}] 👤 {sender}: {message}\n\n"
            self.chat_display.insert(tk.END, formatted_message)
        else:
            formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
            self.chat_display.insert(tk.END, formatted_message)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self):
        #for user to type and send his message
        user_message = self.chat_input.get().strip()
        
        if not user_message:
            return
        
        #To post message to the chat
        self.add_chat_message("You", user_message)
        
        # Clear input
        self.chat_input.delete(0, tk.END)
        
        # Process message with chatbot
        try:
            # Process input using chatbot functions
            processed_input = process_input(user_message)
            pattern = find_pattern(processed_input)
            response = get_response(pattern)
            
            # Post the response of the bot
            self.add_chat_message("Bot", response)
            
        except Exception as e:
            error_response = "Sorry, I encountered an error while processing your message. Please try again."
            self.add_chat_message("Bot", error_response)
        
        # Update status
        self.update_status("Message sent to Bot")


    def clear_chat(self):
        """Clear the chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Add welcome message back
        self.add_chat_message(" Bot",
                             "Chat cleared! Ask me anything about cryptocurrency!")
        
        self.update_status("Chat history cleared")

    def create_data_table(self, parent):
        """Create the data table with scrollbars"""

        # Frame for treeview and scrollbars
        tree_frame = tk.Frame(parent, bg='#f0f0f0')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, show='headings', height=15)

        # Define columns to match the actual CSV column names and order
        columns = ['#', 'Coin', 'Price', '24h', '1h', '7d', 'Market Cap', '24h Volume', 'Timestamp']
        self.tree['columns'] = columns

        # Configure column headings and widths
        column_widths = {
            '#': 50,
            'Coin': 100,
            'Price': 100,
            '24h': 80,
            '1h': 80,
            '7d': 80,
            'Market Cap': 120,
            '24h Volume': 120,
            'Timestamp': 150
        }

        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack everything
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_coin_selected(self, event=None):
        """Handle coin selection from dropdown"""
        try:
            selected_coin = self.selected_coin.get()
            if selected_coin:
                self.filter_data_by_coin(selected_coin)
                self.update_status(f"Show data for: {selected_coin}")
        except Exception as e:
            self.update_status(f"Error during coin selection: {str(e)}")

    def filter_data_by_coin(self, coin_name):
        """Filter and display data for selected coin"""
        if self.current_data is None:
            return

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filter data for the selected coin
        filtered_data = self.current_data[self.current_data['Coin'] == coin_name]

        if filtered_data.empty:
            # If no data found, show a message in the first row
            self.tree.insert('', 'end', values=['', f'No data found for {coin_name}', '', '', '', '', '', '', ''])
            return

        # Insert filtered data into tree - Updated to match CSV column names
        for index, row in filtered_data.iterrows():
            values = [
                row.get('#', ''),
                row.get('Coin', ''),
                row.get('Price', ''),
                row.get('24h', ''),
                row.get('1h', ''),
                row.get('7d', ''),
                row.get('Market Cap', ''),
                row.get('24h Volume', ''),
                row.get('Timestamp', '')
            ]
            self.tree.insert('', 'end', values=values)

    def show_all_coins(self):
        """Show all coins data (reset filter)"""
        try:
            self.populate_data_table()
            self.coin_dropdown.set('')  # Clear selection
            self.update_status("Show all coins")
        except Exception as e:
            self.update_status(f"Error during showing all coins: {str(e)}")

    def load_existing_data(self):
        """Load existing data from CSV file if available"""
        try:
            self.current_data = read_csv_data()
            if self.current_data is not None:
                self.populate_data_table()
                self.update_coin_dropdown()
                self.update_status("Data successfully loaded from CSV file")
            else:
                self.update_status("No current data found - Use 'Scrape New Data'")
        except Exception as e:
            self.update_status(f"Error during data loading: {str(e)}")

    def populate_data_table(self):
        """Populate the data table with current data"""
        if self.current_data is None:
            return

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get latest data (last 10 entries)
        latest_data = self.current_data.tail(10)

        # Insert data into tree - Updated to match CSV column names
        for index, row in latest_data.iterrows():
            values = [
                row.get('#', ''),
                row.get('Coin', ''),
                row.get('Price', ''),
                row.get('24h', ''),
                row.get('1h', ''),
                row.get('7d', ''),
                row.get('Market Cap', ''),
                row.get('24h Volume', ''),
                row.get('Timestamp', '')
            ]
            self.tree.insert('', 'end', values=values)

    def update_coin_dropdown(self):
        """Update the coin dropdown with available coins"""
        try:
            coin_data = get_coin_data_for_dropdown()
            if coin_data:
                coin_names = list(coin_data.keys())
                self.coin_dropdown['values'] = coin_names
                # Don't set a default selection to show all coins initially
        except Exception as e:
            self.update_status(f"Error while updating the list: {str(e)}")

    def scrape_new_data(self):
        """Scrape new cryptocurrency data"""
        try:
            self.update_status("Scraping new data...")
            self.scrape_btn.config(state='disabled')

            # Scrape new data
            new_data = scrape_data()

            if new_data is not None and not new_data.empty:
                self.current_data = new_data
                self.populate_data_table()
                self.update_coin_dropdown()
                self.coin_dropdown.set('')  # Clear selection to show all coins
                self.update_status("New data successfully scraped")
                messagebox.showinfo("Success", "Scrape successful!")
            else:
                self.update_status("Fail during scraping")
                messagebox.showerror("Error", "An error occurred. Please try again.")

        except Exception as e:
            self.update_status(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"Fail during scraping:\n{str(e)}")

        finally:
            self.scrape_btn.config(state='normal')

    def export_data(self):
        """Export current data to CSV"""
        try:
            export_to_csv()
            self.update_status("Data was exported to .csv file")
            messagebox.showinfo("Success", "Data successfully exported to .csv file!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error occurred while exporting to .csv file:\n{str(e)}")

    def show_bar_chart(self):
        show_barchart()

    def show_pie_chart(self):
        show_market_cap_pie()

    def show_line_chart(self):
        show_lineplot()

    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptocurrencyGUI(root)
    root.mainloop()