import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pandas as pd

from scraper import (
    export_to_csv, 
    read_csv_data, 
    top_5_coins_prices, 
    top_5_coins_market_caps, 
    top_5_coins_24h_change,
    top_5_coins_7d_change,
    get_coin_data_for_dropdown
)

class CryptocurrencyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Data Manager")
        self.root.geometry("900x700")
        
        # Αρχικοποίηση μεταβλητών
        self.csv_file_path = r'C:\Users\mario\Desktop\PythonProject\crypto.csv'
        
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
        controls_frame = ttk.LabelFrame(main_frame, text="Έλεγχοι", padding="10")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        controls_frame.columnconfigure(1, weight=1)

        # View selector (αντί για currency selector)
        ttk.Label(controls_frame, text="Επιλέξτε Προβολή:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.view_var = tk.StringVar()
        self.view_combo = ttk.Combobox(controls_frame, textvariable=self.view_var,
                                       values=[
                                           'Όλα τα Δεδομένα',
                                           'Top 5 - Τιμές', 
                                           'Top 5 - Market Caps',
                                           'Top 5 - 24h changes',
                                           'Top 5 - 7d changes'
                                       ],
                                       state='readonly', width=25)
        self.view_combo.grid(row=0, column=1, sticky="w")
        self.view_combo.set('Όλα τα Δεδομένα')
        self.view_combo.bind('<<ComboboxSelected>>', self.on_view_change)

        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)

        self.scrape_btn = ttk.Button(button_frame, text="🔄 Scraping Νέων data", command=self.scrape_data)
        self.scrape_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.chart_btn = ttk.Button(button_frame, text="📊 Εμφάνιση Γραφήματος", command=self.show_chart)
        self.chart_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.export_btn = ttk.Button(button_frame, text="💾 Εξαγωγή in CSV", command=self.export_to_csv_gui)
        self.export_btn.grid(row=0, column=2, padx=5, sticky="ew")

        self.clear_btn = ttk.Button(button_frame, text="🗑️ Καθαρισμός", command=self.clear_data)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.refresh_btn = ttk.Button(button_frame, text="🔄 renew", command=self.refresh_data)
        self.refresh_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky="ew")
        ttk.Label(status_frame, text="Κατάσταση:").grid(row=0, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Έτοιμο για χρήση")
        ttk.Label(status_frame, textvariable=self.status_var, foreground="blue").grid(row=0, column=1, sticky="w")

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=3, column=0, sticky="ew", pady=(5, 15))

        # Data display (treeview) - Δημιουργία με κενές στήλες αρχικά
        data_frame = ttk.LabelFrame(main_frame, text="Δεδομένα Κρυπτονομισμάτων", padding="10")
        data_frame.grid(row=4, column=0, sticky="nsew")
        data_frame.rowconfigure(0, weight=1)
        data_frame.columnconfigure(0, weight=1)

        # Αρχικοποίηση του treeview με βασικές στήλες
        self.setup_treeview(data_frame)

    def setup_treeview(self, parent, columns=None):
        """Δημιουργεί ή ενημερώνει το treeview με τις κατάλληλες στήλες"""
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
        """Φορτώνει αρχικά δεδομένα από το CSV αν υπάρχει"""
        try:
            df = read_csv_data(self.csv_file_path)
            if df is not None and not df.empty:
                self.display_dataframe(df.tail(10))  # Εμφανίζει τα τελευταία 10 εγγραφές
                self.status_var.set("Φορτώθηκαν υπάρχοντα δεδομένα")
            else:
                self.status_var.set("Δεν βρέθηκαν υπάρχοντα δεδομένα")
        except Exception as e:
            self.status_var.set(f"error φόρτωσης: {str(e)}")

    def display_dataframe(self, df):
        """Εμφανίζει ένα DataFrame στο treeview"""
        # Καθαρισμός υπαρχουσών εγγραφών
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Προσθήκη νέων data
        for _, row in df.iterrows():
            values = [str(row[col]) if col in row else '' for col in self.tree['columns']]
            self.tree.insert('', 'end', values=values)

    def scrape_data(self):
        """Εκτελεί scraping in ξεχωριστό thread"""
        def scrape_thread():
            try:
                self.scrape_btn.config(state='disabled')
                self.status_var.set("Γίνεται scraping data...")
                self.progress['value'] = 20
                
                # Εκτέλεση του scraping
                export_to_csv()
                
                self.progress['value'] = 80
                
                # renew της εμφάνισης
                self.refresh_data()
                
                self.progress['value'] = 100
                self.status_var.set("Scraping ολοκληρώθηκε επιτυχώς!")
                
            except Exception as e:
                self.status_var.set(f"error scraping: {str(e)}")
                messagebox.showerror("error", f"Προέκυψε error κατά το scraping:\n{str(e)}")
            finally:
                self.scrape_btn.config(state='normal')
                self.progress['value'] = 0
        
        # Εκτέλεση in ξεχωριστό thread για να μην κολλήinι το GUI
        threading.Thread(target=scrape_thread, daemon=True).start()

    def on_view_change(self, event=None):
        """Αλλάζει την εμφάνιση βάinι της επιλογής του χρήστη"""
        selected_view = self.view_var.get()
        
        try:
            if selected_view == 'Όλα τα Δεδομένα':
                df = read_csv_data(self.csv_file_path)
                if df is not None:
                    self.display_dataframe(df.tail(10))
                    
            elif selected_view == 'Top 5 - Τιμές':
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
                    
            self.status_var.set(f"Εμφάνιση: {selected_view}")
            
        except Exception as e:
            self.status_var.set(f"error εμφάνισης: {str(e)}")

    def show_chart(self):
        """Εμφάνιση γραφήματος - για μελλοντική υλοποίηση"""
        messagebox.showinfo("Γράφημα", "Η λειτουργία γραφήματος θα υλοποιηθεί σύντομα!")
        self.status_var.set("Γράφημα - Δεν είναι διαθέσιμο ακόμη")

    def export_to_csv_gui(self):
        """Wrapper για την εξαγωγή CSV με GUI feedback"""
        try:
            self.status_var.set("Εξαγωγή in CSV...")
            self.progress['value'] = 50
            
            # Η export_to_csv() ήδη αποθηκεύει στο αρχείο
            # Εδώ μπορούμε να προσθέσουμε επιπλέον λειτουργικότητα αν χρειαστεί
            
            self.progress['value'] = 100
            self.status_var.set("Εξαγωγή ολοκληρώθηκε")
            messagebox.showinfo("Επιτυχία", f"Τα δεδομένα εξήχθησαν στο:\n{self.csv_file_path}")
            
        except Exception as e:
            self.status_var.set(f"error εξαγωγής: {str(e)}")
            messagebox.showerror("error", f"error εξαγωγής:\n{str(e)}")
        finally:
            self.progress['value'] = 0

    def clear_data(self):
        """Καθαρίζει τα εμφανιζόμενα δεδομένα"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_var.set("Καθαρίστηκαν τα δεδομένα από την εμφάνιση")

    def refresh_data(self):
        """Ανανεώνει τα δεδομένα από το CSV"""
        try:
            self.status_var.set("renew data...")
            
            # renew βάinι της τρέχουσας προβολής
            self.on_view_change()
            
            self.status_var.set("Δεδομένα ανανεώθηκαν")
            
        except Exception as e:
            self.status_var.set(f"error renewς: {str(e)}")

# Main launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptocurrencyGUI(root)
    root.mainloop()