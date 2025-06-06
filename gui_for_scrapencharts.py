import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from scraper import (
    export_to_csv, 
    read_csv_data, 
    top_5_coins_prices, 
    top_5_coins_market_caps, 
    top_5_coins_24h_change,
    top_5_coins_7d_change,
    get_coin_data_for_dropdown
)

# functions from graphs.py
from graphs import create_sample_data, create_bar_chart, create_pie_chart, create_line_plot

class CryptocurrencyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Data Manager")
        self.root.geometry("900x700")
        
        # initializing variables
        self.csv_file_path = r'C:\Users\mario\Desktop\PythonProject\crypto.csv'
        self.current_chart_window = None
        
        self.create_widgets()
        self.load_initial_data()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weight for resizing
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cryptocurrency Data Manager", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Checks", padding="10")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        controls_frame.columnconfigure(1, weight=1)

        # View selector
        ttk.Label(controls_frame, text="Select view:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.view_var = tk.StringVar()
        self.view_combo = ttk.Combobox(controls_frame, textvariable=self.view_var,
                                       values=[
                                           'All data',
                                           'Top 5 - Prices', 
                                           'Top 5 - Market Caps',
                                           'Top 5 - 24h changes',
                                           'Top 5 - 7d changes'
                                       ],
                                       state='readonly', width=25)
        self.view_combo.grid(row=0, column=1, sticky="w")
        self.view_combo.set('All data')
        self.view_combo.bind('<<ComboboxSelected>>', self.on_view_change)

        # Chart type selector
        ttk.Label(controls_frame, text= "type of graph :").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.chart_type_var = tk.StringVar()
        self.chart_type_combo = ttk.Combobox(controls_frame, textvariable=self.chart_type_var,
                                           values=[
                                               'Bar Chart - Τιμές Top 5',
                                               'Pie Chart - Market Caps Top 5', 
                                               'Line Plot - changes Top 5',
                                               'all graphs'
                                           ],
                                           state='readonly', width=25)
        self.chart_type_combo.grid(row=0, column=3, sticky="w")
        self.chart_type_combo.set('Bar Chart - Prices Top 5')

        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky="ew")
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

        self.scrape_btn = ttk.Button(button_frame, text=" Scraping New Data", command=self.scrape_data)
        self.scrape_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.chart_btn = ttk.Button(button_frame, text=" Show graph", command=self.show_chart)
        self.chart_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.export_btn = ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv_gui)
        self.export_btn.grid(row=0, column=2, padx=5, sticky="ew")

        self.sample_chart_btn = ttk.Button(button_frame, text="Sample Graphs", command=self.show_sample_charts)
        self.sample_chart_btn.grid(row=0, column=3, padx=5, sticky="ew")

        self.clear_btn = ttk.Button(button_frame, text=" Clear ", command=self.clear_data)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.refresh_btn = ttk.Button(button_frame, text="renew", command=self.refresh_data)
        self.refresh_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky="ew")
        ttk.Label(status_frame, text=" Status:").grid(row=0, column=0, sticky="w")
        self.status_var = tk.StringVar(value=" Ready for use")
        ttk.Label(status_frame, textvariable=self.status_var, foreground="blue").grid(row=0, column=1, sticky="w")

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=3, column=0, sticky="ew", pady=(5, 15))

        # Data display (treeview)
        data_frame = ttk.LabelFrame(main_frame, text="Types of cryptos", padding="10")
        data_frame.grid(row=4, column=0, sticky="nsew")
        data_frame.rowconfigure(0, weight=1)
        data_frame.columnconfigure(0, weight=1)

        self.setup_treeview(data_frame)

    def setup_treeview(self, parent, columns=None):
        
        if hasattr(self, 'tree'):
            self.tree.destroy()
        if hasattr(self, 'vsb'):
            self.vsb.destroy()
            
        if columns is None:
            columns = ['#', 'Coin', 'Price', 'Market Cap', '24h', '7d', 'Volume', 'Timestamp']
        
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # Ρύθmiση στηλών
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ['Price', 'Market Cap', 'Volume']:
                self.tree.column(col, width=120)
            elif col == 'Timestamp':
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=80)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.vsb.set)

    def load_initial_data(self):
        #from csv
        try:
            df = read_csv_data(self.csv_file_path)
            if df is not None and not df.empty:
                self.display_dataframe(df.tail(10))
                self.status_var.set("Data loaded")
            else:
                self.status_var.set("No data founf")
        except Exception as e:
            self.status_var.set(f"Error in load: {str(e)}")

    def display_dataframe(self, df):
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for _, row in df.iterrows():
            values = [str(row[col]) if col in row else '' for col in self.tree['columns']]
            self.tree.insert('', 'end', values=values)

    def scrape_data(self):
        
        def scrape_thread():
            try:
                self.scrape_btn.config(state='disabled')
                self.status_var.set("Scraping data...")
                self.progress['value'] = 20
                
                export_to_csv()
                
                self.progress['value'] = 80
                self.refresh_data()
                
                self.progress['value'] = 100
                self.status_var.set("Scraping done!")
                
            except Exception as e:
                self.status_var.set(f"error scraping: {str(e)}")
                messagebox.showerror("error", f" error κατά το scraping:\n{str(e)}")
            finally:
                self.scrape_btn.config(state='normal')
                self.progress['value'] = 0
        
        threading.Thread(target=scrape_thread, daemon=True).start()

    def on_view_change(self, event=None):
       
        selected_view = self.view_var.get()
        
        try:
            if selected_view == 'All data':
                df = read_csv_data(self.csv_file_path)
                if df is not None:
                    self.display_dataframe(df.tail(10))
                    
            elif selected_view == 'Top 5 - Prices':
                df = top_5_coins_prices(self.csv_file_path)
                if df is not None:
                    self.setup_treeview(self.tree.master, ['Coin', 'Price'])
                    self.display_dataframe(df)
                    
            elif selected_view == 'Top 5 - Market Caps':
                df = top_5_coins_market_caps(self.csv_file_path)
                if df is not None:
                    self.setup_treeview(self.tree.master, ['Coin', 'Market Cap'])
                    self.display_dataframe(df)
                    
            elif selected_view == 'Top 5 - 24h changes':
                df = top_5_coins_24h_change(self.csv_file_path)
                if df is not None:
                    self.setup_treeview(self.tree.master, ['Coin', '24h'])
                    self.display_dataframe(df)
                    
            elif selected_view == 'Top 5 - 7d changes':
                df = top_5_coins_7d_change(self.csv_file_path)
                if df is not None:
                    self.setup_treeview(self.tree.master, ['Coin', '7d'])
                    self.display_dataframe(df)
                    
            self.status_var.set(f"View: {selected_view}")
            
        except Exception as e:
            self.status_var.set(f"error viewing: {str(e)}")

    def convert_csv_to_graphs_format(self, df):
       
        try:
            # CSV has : Coin, Price, Market Cap, 24h, 7d
            graph_data = {
                'name': df['Coin'].tolist() if 'Coin' in df.columns else [],
                'price_in_usd': df['Price'].tolist() if 'Price' in df.columns else [],
                'change_in_24h': df['24h'].tolist() if '24h' in df.columns else [],
                'change_in_7d': df['7d'].tolist() if '7d' in df.columns else [],
                'market_cap': df['Market Cap'].tolist() if 'Market Cap' in df.columns else []
            }
            return pd.DataFrame(graph_data)
        except Exception as e:
            print(f"error converting data: {e}")
            return None

    def show_chart(self):
        
        try:
            chart_type = self.chart_type_var.get()
            
            # Load data from CSV
            df = read_csv_data(self.csv_file_path)
            if df is None or df.empty:
                messagebox.showwarning("Warning", "No data, can't create a graph")
                return
            
            # Convert data to match graphs.py
            graph_df = self.convert_csv_to_graphs_format(df)
            if graph_df is None:
                messagebox.showerror("error", "Converting data not possible")
                return
            
            self.status_var.set("Creating graph")
            
            if chart_type == 'Bar Chart - Prices Top 5':
                self.create_custom_bar_chart(graph_df)
            elif chart_type == 'Pie Chart - Market Caps Top 5':
                self.create_custom_pie_chart(graph_df)
            elif chart_type == 'Line Plot - changes Top 5':
                self.create_custom_line_plot(graph_df)
            elif chart_type == 'All graphs':
                self.show_all_charts(graph_df)
            
            self.status_var.set("Here's your graph")
            
        except Exception as e:
            self.status_var.set(f"graph error: {str(e)}")
            messagebox.showerror("error", f"error viewing graph:\n{str(e)}")

    def create_custom_bar_chart(self, df):
       
        if df.empty or 'price_in_usd' not in df.columns:
            messagebox.showwarning("Warning", "No data")
            return
            
        top_5 = df.nlargest(5, 'price_in_usd')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_5['name'], top_5['price_in_usd'], color='orange')
        ax.set_title('Prices for top 5 cryptos')
        ax.set_xlabel('Crypto')
        ax.set_ylabel('Price in USD')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self.show_chart_in_window(fig, "Bar Chart - Prices")

    def create_custom_pie_chart(self, df):
        
        if df.empty or 'market_cap' not in df.columns:
            messagebox.showwarning("Warning", "No data for capitalization!")
            return
            
        top_5 = df.nlargest(5, 'market_cap')
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(top_5['market_cap'], labels=top_5['name'], autopct='%1.1f%%')
        ax.set_title('distribution of Top 5 capitalized cryptos')
        
        self.show_chart_in_window(fig, "Pie Chart - Market Caps")

    def create_custom_line_plot(self, df):
        
        if df.empty or 'change_in_24h' not in df.columns or 'change_in_7d' not in df.columns:
            messagebox.showwarning("Warning", "No data!")
            return
            
        top_5 = df.nlargest(5, 'market_cap')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(top_5['name'], top_5['change_in_24h'], marker='o', label='change in 24h')
        ax.plot(top_5['name'], top_5['change_in_7d'], marker='s', label='change in 7d')
        ax.set_title('changes of prices/ top 5 cryptos')
        ax.set_xlabel('Cryptos')
        ax.set_ylabel('Percentage of change(%)')
        ax.legend()
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        self.show_chart_in_window(fig, "Line Plot - changes")

    def show_all_charts(self, df):
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Bar Chart
        if 'price_in_usd' in df.columns:
            top_5_price = df.nlargest(5, 'price_in_usd')
            ax1.bar(top_5_price['name'], top_5_price['price_in_usd'], color='orange')
            ax1.set_title('Top 5 Τιμές')
            ax1.tick_params(axis='x', rotation=45)
        
        # Pie Chart
        if 'market_cap' in df.columns:
            top_5_cap = df.nlargest(5, 'market_cap')
            ax2.pie(top_5_cap['market_cap'], labels=top_5_cap['name'], autopct='%1.1f%%')
            ax2.set_title('Top 5 Market Caps')
        
        # Line Plot
        if 'change_in_24h' in df.columns and 'change_in_7d' in df.columns:
            top_5_change = df.nlargest(5, 'market_cap')
            ax3.plot(top_5_change['name'], top_5_change['change_in_24h'], marker='o', label='24h')
            ax3.plot(top_5_change['name'], top_5_change['change_in_7d'], marker='s', label='7d')
            ax3.set_title('changes τιμών')
            ax3.legend()
            ax3.tick_params(axis='x', rotation=45)
            ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax3.grid(True, alpha=0.3)
        
        # hide fourth subplot
        ax4.axis('off')
        
        plt.tight_layout()
        self.show_chart_in_window(fig, "All graphs")

    def show_chart_in_window(self, fig, title):
       
        if self.current_chart_window:
            self.current_chart_window.destroy()
        
        self.current_chart_window = tk.Toplevel(self.root)
        self.current_chart_window.title(f"Graph - {title}")
        self.current_chart_window.geometry("800x600")
        
        canvas = FigureCanvasTkAgg(fig, self.current_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        
        close_btn = ttk.Button(self.current_chart_window, text="Close", 
                              command=self.current_chart_window.destroy)
        close_btn.pack(pady=10)

#export to csv with gui
    def export_to_csv_gui(self):
        
        try:
            self.status_var.set("Exporting in CSV...")
            self.progress['value'] = 50
            self.progress['value'] = 100
            self.status_var.set("Export done")
            messagebox.showinfo("Success", f"Data exported in:\n{self.csv_file_path}")
            
        except Exception as e:
            self.status_var.set(f"error during export: {str(e)}")
            messagebox.showerror("error", f"error during export:\n{str(e)}")
        finally:
            self.progress['value'] = 0

    def clear_data(self):
        #clear data that is shown
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_var.set("Data is cleared")

#refreshing the data from the csv
    def refresh_data(self):
        
        try:
            self.status_var.set("renew data...")
            self.on_view_change()
            self.status_var.set("Data renewd")
        except Exception as e:
            self.status_var.set(f"error renewς: {str(e)}")

# Main launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptocurrencyGUI(root)
    root.mainloop()