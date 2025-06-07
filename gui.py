import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pandas as pd
from scraper import (
    scrape_data,
    export_to_csv,
    read_csv_data,
    get_coin_data_for_dropdown,
    top_5_coins_prices,
    top_5_coins_market_caps,
    top_5_coins_24h_change,
    top_5_coins_7d_change
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from graphs import (
show_market_cap_pie,
show_barchart,
show_lineplot
)

# Import chatbot functions
from chatbot import process_input, find_pattern, get_response

class CryptocurrencyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Tracker & Chatbot - Αναλυτής Κρυπτονομισμάτων")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Initialize data
        self.current_data = None
        self.selected_coin = tk.StringVar()

        # Create the main interface
        self.create_widgets()

        # Load initial data if available
        self.load_existing_data()

    def create_widgets(self):
        """Create all GUI widgets"""

        # Title
        title_label = tk.Label(
            self.root,
            text="Cryptocurrency Data Tracker & Crypto Assistant",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)

        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Data Analysis Tab
        self.data_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.data_tab, text="📊 Data Analysis")

        # Create Chatbot Tab
        self.chat_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.chat_tab, text="🤖 Assistant")

        # Setup Data Analysis Tab
        self.setup_data_tab()

        # Setup Chatbot Tab
        self.setup_chat_tab()

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Έτοιμο - Φορτώστε δεδομένα για να ξεκινήσετε",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#bdc3c7',
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_data_tab(self):
        """Setup the data analysis tab (original functionality)"""
        # Main frame for data tab
        main_frame = tk.Frame(self.data_tab, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel for controls
        left_panel = tk.Frame(main_frame, bg='#ecf0f1', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Control buttons section
        control_frame = tk.LabelFrame(left_panel, text="Έλεγχος Δεδομένων", font=("Arial", 12, "bold"), bg='#ecf0f1')
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Scrape data button
        self.scrape_btn = tk.Button(
            control_frame,
            text="🔄 Συλλογή Νέων Δεδομένων",
            command=self.scrape_new_data,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=5
        )
        self.scrape_btn.pack(fill=tk.X, padx=5, pady=5)

        # Export data button
        self.export_btn = tk.Button(
            control_frame,
            text="💾 Εξαγωγή σε CSV",
            command=self.export_data,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=5
        )
        self.export_btn.pack(fill=tk.X, padx=5, pady=5)

        # Coin selection section
        selection_frame = tk.LabelFrame(left_panel, text="Επιλογή Νομίσματος", font=("Arial", 12, "bold"), bg='#ecf0f1')
        selection_frame.pack(fill=tk.X, padx=10, pady=10)

        # Dropdown for coin selection
        tk.Label(selection_frame, text="Επιλέξτε Κρυπτονόμισμα:", bg='#ecf0f1', font=("Arial", 10)).pack(pady=5)

        self.coin_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_coin,
            state="readonly",
            font=("Arial", 10)
        )
        self.coin_dropdown.pack(fill=tk.X, padx=5, pady=5)
        # Bind the dropdown selection event
        self.coin_dropdown.bind('<<ComboboxSelected>>', self.on_coin_selected)

        # Add "Show All" button
        self.show_all_btn = tk.Button(
            selection_frame,
            text="Εμφάνιση Όλων",
            command=self.show_all_coins,
            bg='#34495e',
            fg='white',
            font=("Arial", 9),
            pady=3
        )
        self.show_all_btn.pack(fill=tk.X, padx=5, pady=5)

        # Charts section
        charts_frame = tk.LabelFrame(left_panel, text="Γραφήματα & Ανάλυση", font=("Arial", 12, "bold"), bg='#ecf0f1')
        charts_frame.pack(fill=tk.X, padx=10, pady=10)

        # Chart buttons
        self.bar_chart_btn = tk.Button(
            charts_frame,
            text="📊 Bar Chart - Τιμές Top 5",
            command=self.show_bar_chart,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.bar_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        self.pie_chart_btn = tk.Button(
            charts_frame,
            text="🥧 Pie Chart - Market Cap",
            command=self.show_pie_chart,
            bg='#9b59b6',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.pie_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        self.line_chart_btn = tk.Button(
            charts_frame,
            text="📈 Line Plot - Μεταβολές",
            command=self.show_line_chart,
            bg='#f39c12',
            fg='white',
            font=("Arial", 10, "bold"),
            pady=3
        )
        self.line_chart_btn.pack(fill=tk.X, padx=5, pady=2)

        # Right panel for data display
        right_panel = tk.Frame(main_frame, bg='#f0f0f0')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Data table section
        table_frame = tk.LabelFrame(right_panel, text="Δεδομένα Κρυπτονομισμάτων", font=("Arial", 12, "bold"),
                                    bg='#f0f0f0')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Treeview for data display
        self.create_data_table(table_frame)

    def setup_chat_tab(self):
        """Setup the chatbot tab"""
        # Main chat frame
        chat_main_frame = tk.Frame(self.chat_tab, bg='#f0f0f0')
        chat_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Chat title
        chat_title = tk.Label(
            chat_main_frame,
            text="🤖 Cryptocurrency Assistant",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        chat_title.pack(pady=(0, 20))

        # Chat display area
        chat_display_frame = tk.LabelFrame(
            chat_main_frame, 
            text="Conversation", 
            font=("Arial", 12, "bold"),
            bg='#f0f0f0'
        )
        chat_display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(
            chat_display_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 11),
            bg='#ffffff',
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
            bg='#f0f0f0',
            fg='#34495e'
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))

        # Input entry frame
        entry_frame = tk.Frame(input_frame, bg='#f0f0f0')
        entry_frame.pack(fill=tk.X)

        # Chat input entry
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
            text="Send 📤",
            command=self.send_message,
            bg='#3498db',
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

        # Clear chat button
        self.clear_chat_btn = tk.Button(
            control_buttons_frame,
            text="🗑️ Clear Chat",
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

        # Quick question buttons
        quick_questions = [
            ("What is cryptocurrency?", "explain crypto"),
            ("Bitcoin price info", "bitcoin price"),
            ("Investment advice", "investment advice"),
            ("App usage help", "how to use app")
        ]

        quick_buttons_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        quick_buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        for i, (display_text, question) in enumerate(quick_questions):
            btn = tk.Button(
                quick_buttons_frame,
                text=display_text,
                command=lambda q=question: self.send_quick_question(q),
                bg='#95a5a6',
                fg='white',
                font=("Arial", 9),
                pady=2,
                relief=tk.RAISED,
                bd=1
            )
            btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Add welcome message
        self.add_chat_message("🤖 Assistant",
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
        """Send user message and get chatbot response"""
        user_message = self.chat_input.get().strip()
        
        if not user_message:
            return
        
        # Add user message to chat
        self.add_chat_message("You", user_message)
        
        # Clear input
        self.chat_input.delete(0, tk.END)
        
        # Process message with chatbot
        try:
            # Process input using chatbot functions
            processed_input = process_input(user_message)
            pattern = find_pattern(processed_input)
            response = get_response(pattern)
            
            # Add bot response to chat
            self.add_chat_message("🤖 Assistant", response)
            
        except Exception as e:
            error_response = "Sorry, I encountered an error while processing your message. Please try again."
            self.add_chat_message("🤖 Assistant", error_response)
        
        # Update status
        self.update_status("Message sent to Assistant")

    def send_quick_question(self, question):
        """Send a quick question"""
        self.chat_input.delete(0, tk.END)
        self.chat_input.insert(0, question)
        self.send_message()

    def clear_chat(self):
        """Clear the chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Add welcome message back
        self.add_chat_message("🤖 Assistant",
                             "Chat cleared! Ask me anything about cryptocurrency!")
        
        self.update_status("Chat history cleared")

    def create_data_table(self, parent):
        """Create the data table with scrollbars"""

        # Frame for treeview and scrollbars
        tree_frame = tk.Frame(parent, bg='#f0f0f0')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, show='headings', height=15)

        # Define columns
        columns = ['#', 'Coin', 'Price', '24h', '7d', 'Market Cap', 'Volume', 'Timestamp']
        self.tree['columns'] = columns

        # Configure column headings and widths
        column_widths = {
            '#': 50,
            'Coin': 100,
            'Price': 100,
            '24h': 80,
            '7d': 80,
            'Market Cap': 120,
            'Volume': 120,
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
                self.update_status(f"Εμφάνιση δεδομένων για: {selected_coin}")
        except Exception as e:
            self.update_status(f"Σφάλμα κατά την επιλογή νομίσματος: {str(e)}")

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
            self.tree.insert('', 'end', values=['', f'Δεν βρέθηκαν δεδομένα για {coin_name}', '', '', '', '', '', ''])
            return

        # Insert filtered data into tree
        for index, row in filtered_data.iterrows():
            values = [
                row.get('#', ''),
                row.get('Coin', ''),
                row.get('Price', ''),
                row.get('24h', ''),
                row.get('7d', ''),
                row.get('Market Cap', ''),
                row.get('Volume', ''),
                row.get('Timestamp', '')
            ]
            self.tree.insert('', 'end', values=values)

    def show_all_coins(self):
        """Show all coins data (reset filter)"""
        try:
            self.populate_data_table()
            self.coin_dropdown.set('')  # Clear selection
            self.update_status("Εμφάνιση όλων των κρυπτονομισμάτων")
        except Exception as e:
            self.update_status(f"Σφάλμα κατά την εμφάνιση όλων: {str(e)}")

    def load_existing_data(self):
        """Load existing data from CSV file if available"""
        try:
            self.current_data = read_csv_data()
            if self.current_data is not None:
                self.populate_data_table()
                self.update_coin_dropdown()
                self.update_status("Δεδομένα φορτώθηκαν επιτυχώς από το αρχείο CSV")
            else:
                self.update_status("Δεν βρέθηκαν υπάρχοντα δεδομένα - Χρησιμοποιήστε 'Συλλογή Νέων Δεδομένων'")
        except Exception as e:
            self.update_status(f"Σφάλμα κατά τη φόρτωση δεδομένων: {str(e)}")

    def populate_data_table(self):
        """Populate the data table with current data"""
        if self.current_data is None:
            return

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get latest data (last 10 entries)
        latest_data = self.current_data.tail(10)

        # Insert data into tree
        for index, row in latest_data.iterrows():
            values = [
                row.get('#', ''),
                row.get('Coin', ''),
                row.get('Price', ''),
                row.get('24h', ''),
                row.get('7d', ''),
                row.get('Market Cap', ''),
                row.get('Volume', ''),
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
            self.update_status(f"Σφάλμα κατά την ενημέρωση λίστας νομισμάτων: {str(e)}")

    def scrape_new_data(self):
        """Scrape new cryptocurrency data"""
        try:
            self.update_status("Συλλογή νέων δεδομένων...")
            self.scrape_btn.config(state='disabled')

            # Scrape new data
            new_data = scrape_data()

            if new_data is not None and not new_data.empty:
                self.current_data = new_data
                self.populate_data_table()
                self.update_coin_dropdown()
                self.coin_dropdown.set('')  # Clear selection to show all coins
                self.update_status("Νέα δεδομένα συλλέχθηκαν επιτυχώς!")
                messagebox.showinfo("Επιτυχία", "Τα νέα δεδομένα συλλέχθηκαν επιτυχώς!")
            else:
                self.update_status("Αποτυχία συλλογής δεδομένων")
                messagebox.showerror("Σφάλμα", "Αποτυχία συλλογής δεδομένων. Παρακαλώ δοκιμάστε ξανά.")

        except Exception as e:
            self.update_status(f"Σφάλμα κατά τη συλλογή δεδομένων: {str(e)}")
            messagebox.showerror("Σφάλμα", f"Σφάλμα κατά τη συλλογή δεδομένων:\n{str(e)}")

        finally:
            self.scrape_btn.config(state='normal')

    def export_data(self):
        """Export current data to CSV"""
        try:
            export_to_csv()
            self.update_status("Δεδομένα εξήχθησαν στο CSV αρχείο")
            messagebox.showinfo("Επιτυχία", "Τα δεδομένα εξήχθησαν επιτυχώς στο CSV αρχείο!")
        except Exception as e:
            self.update_status(f"Σφάλμα κατά την εξαγωγή: {str(e)}")
            messagebox.showerror("Σφάλμα", f"Σφάλμα κατά την εξαγωγή δεδομένων:\n{str(e)}")

    def export_custom_csv(self):
        """Export data to a custom location"""
        try:
            if self.current_data is None:
                messagebox.showwarning("Προειδοποίηση", "Δεν υπάρχουν δεδομένα για εξαγωγή!")
                return

            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Αποθήκευση CSV αρχείου"
            )

            if file_path:
                # Get latest data
                latest_data = self.current_data.tail(10)
                latest_data.to_csv(file_path, index=False)
                self.update_status(f"Δεδομένα εξήχθησαν στο: {file_path}")
                messagebox.showinfo("Επιτυχία", f"Τα δεδομένα αποθηκεύτηκαν επιτυχώς στο:\n{file_path}")

        except Exception as e:
            self.update_status(f"Σφάλμα κατά την προσαρμοσμένη εξαγωγή: {str(e)}")
            messagebox.showerror("Σφάλμα", f"Σφάλμα κατά την εξαγωγή:\n{str(e)}")

    def refresh_data_table(self):
        """Refresh the data table with latest data from CSV"""
        try:
            self.current_data = read_csv_data()
            if self.current_data is not None:
                self.populate_data_table()
                self.update_coin_dropdown()
                self.update_status("Πίνακας δεδομένων ανανεώθηκε")
            else:
                self.update_status("Δεν βρέθηκαν δεδομένα για ανανέωση")
        except Exception as e:
            self.update_status(f"Σφάλμα κατά την ανανέωση: {str(e)}")

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


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CryptocurrencyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()