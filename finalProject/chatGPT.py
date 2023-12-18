import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import requests

class ExpensesTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("$ EXPENSES TRACKER")
        self.configure_layout()

        label_font = ("Helvetica", 16)

        labels = ["Amount", "Currency", "Category", "Payment Method", "Date"]
        self.widgets = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, text=label_text + ":", font=label_font, bg='LightGray')
            label.grid(row=i, rowspan=1, column=0, padx=0, pady=0, sticky="nsew")

            if label_text == "Amount":
                entry = tk.Entry(self.root, width=23)
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            elif label_text == "Currency":
                values = ["USD", "GBP", "EGP", "SAR", "AED", "gas"]
                entry = ttk.Combobox(self.root, values=values, state='readonly')
                entry.set(values[0])
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            elif label_text == "Category":
                values = ["savings", "life expenses", "education", "grocery", "electricity", "gas", "rental", "charity"]
                entry = ttk.Combobox(self.root, values=values, state='readonly')
                entry.set(values[0])
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            elif label_text == "Payment Method":
                values = ["Cash", "Credit Card", "Paypal"]
                entry = ttk.Combobox(self.root, values=values, state='readonly')
                entry.set(values[0])
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            elif label_text == "Date":
                entry = DateEntry(self.root, width=20)
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")

            self.widgets[label_text.lower().replace(" ", "_")] = entry

        add_expenses_button = tk.Button(self.root, text="Add Expenses", bg="#4CAF50", fg="white", font=label_font,
                                        command=self.add_expenses)
        add_expenses_button.grid(row=5, column=1, padx=40, pady=10, sticky="w")

        # Create a Text widget for displaying the conversion results
        self.result_text = tk.Text(self.root, height=5, width=40, bg="#FFD700", font=("Helvetica", 12),
                                   relief="solid", borderwidth=1)
        self.result_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        columns = ("Amount", "Currency", "Category", "Payment Method", "Datetime")
        self.tree = ttk.Treeview(self.root, columns=columns, height=20)
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        for col in columns:
            self.tree.heading(col, text=col.title())

        # Add the following line to make the Treeview expand horizontally
        self.root.columnconfigure(0, weight=1)

        self.index = 0

    def configure_layout(self):
        for i in range(5):
            self.root.rowconfigure(i, minsize=5, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, minsize=10, weight=1)
        self.root.configure(padx=0, pady=0, bg='LightGray')

    def add_expenses(self):
        # Delete the previous total in USD
        self.result_text.delete(1.0, tk.END)

        expenses_details = self.get_expenses()

        if expenses_details:
            self.tree.insert('', tk.END, iid=self.index, values=expenses_details[0:])
            self.index += 1

        # Accumulate the total USD amount
        total_usd = sum(self.fetch_data(amount, currency) for item_id in self.tree.get_children()
                        for amount, currency in [self.tree.item(item_id, "values")[:2]])

        # Display the total USD amount
        total_text = f'Total in USD: {total_usd:.2f} USD\n'
        self.result_text.insert(tk.END, total_text)

    def get_expenses(self):
        try:
            amount = float(self.widgets['amount'].get())
            if amount >= 0:
                return [amount,
                        self.widgets['currency'].get(),
                        self.widgets['category'].get(),
                        self.widgets['payment_method'].get(),
                        self.widgets['date'].get()]
            else:
                messagebox.showerror("Error", "Enter a valid numeric amount as expenses")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric amount as expenses")

        return None

    def fetch_data(self, amount, currency):
        try:
            amount = float(amount)
        except ValueError:
            amount = simpledialog.askfloat("Invalid Amount", "Enter a valid numeric amount:")

        if amount <= 0:
            amount = simpledialog.askfloat("Invalid Amount", "Enter a valid amount greater than 0:")

        # Replace the placeholder API key and adjust the URL accordingly
        url = f"https://api.apilayer.com/fixer/convert?to=USD&from={currency}&amount={amount}"
        headers = {"apikey": "yy7eTIMbsRLnwxHu8WZ7UgsncczcHP7f"}  # Replace with your actual API key

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Sorry, there was a problem. Please try again later.")
            quit()

        result = response.json()
        converted_amount = result.get('result', 0.0)
        return converted_amount


if __name__ == "__main__":
    root = tk.Tk()

    # Set the initial size of the window
    root.geometry("1000x800")
    expenses_tracker = ExpensesTrackerApp(root)
    root.mainloop()
