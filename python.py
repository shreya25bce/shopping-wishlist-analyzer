import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, os, datetime
import matplotlib.pyplot as plt

from datetime import datetime, timedelta, timezone

def get_today_ist():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y/%m/%d")

class WishlistAnalyzer:
    CATEGORIES = ["Electronics", "Books", "Groceries", "Clothes", "Stationery", "Other"]

    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Wishlist Cost Analyzer")
        self.theme = "dark"
        self.username = None
        self.filename = None
        self.items = []
        self.budget = None
        self.set_theme(self.theme)
        self.root.bind("<F2>", lambda e: self.admin_window())
        self.ask_username()

    def set_theme(self, theme):
        if theme == "dark":
            self.bg = "#24292F"
            self.entry_bg = "#2D333B"
            self.entry_fg = "#D1D5DA"
            self.btn_bg = "#36B37E"
            self.btn_fg = "black"
            self.header_bg = "#36B37E"
            self.header_fg = "black"
            self.table_bg = "#34344A"
            self.table_fg = "#FFD6E0"
            self.warning_fg = "#D6336C"
        else:
            self.bg = "#EAEAEA"
            self.entry_bg = "#FFFFFF"
            self.entry_fg = "#24292F"
            self.btn_bg = "#85C7F2"
            self.btn_fg = "black"
            self.header_bg = "#B2D7FF"
            self.header_fg = "black"
            self.table_bg = "#E5F4F6"
            self.table_fg = "#24292F"
            self.warning_fg = "red"
        try: self.root.configure(bg=self.bg)
        except Exception: pass

    def set_widget_theme(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, (tk.Label, tk.Button, tk.Entry, tk.Toplevel, tk.Frame)):
                try: child.configure(bg=self.bg, fg=self.entry_fg)
                except Exception: pass

    def ask_username(self):
        win = tk.Toplevel(self.root)
        self.set_widget_theme(win)
        win.title("Enter Username")
        tk.Label(win, text="Enter username (or admin):", bg=self.bg, fg=self.entry_fg).pack(pady=6)
        entry = tk.Entry(win, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        entry.pack(pady=6)
        budget_label = tk.Label(win, text="Enter budget (optional):", bg=self.bg, fg=self.entry_fg)
        budget_label.pack()
        budget_entry = tk.Entry(win, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        budget_entry.pack()
        def submit():
            name = entry.get().strip()
            self.budget = budget_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a username.")
                return
            if name.lower() == "admin":
                win.destroy()
                self.admin_window()
            else:
                self.username = name
                self.filename = f"{self.username}_wishlist.csv"
                win.destroy()
                self.init_main_ui()
                self.load_items()
                self.refresh_tree()
                self.update_total()
        tk.Button(win, text="Done", command=submit, bg="#F64C72", fg="black").pack(pady=8)

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.set_theme(self.theme)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Toplevel, tk.Frame)):
                try: widget.configure(bg=self.bg, fg=self.entry_fg)
                except Exception: pass
        self.update_tree_style()
        self.refresh_tree()

    def update_tree_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=self.table_bg, fieldbackground=self.table_bg, foreground=self.table_fg, rowheight=28, bordercolor=self.btn_bg, borderwidth=1)
        style.configure("Treeview.Heading", background=self.header_bg, foreground=self.header_fg, font=("Arial", 11, "bold"))
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.map("Treeview", background=[("selected", self.entry_bg)])

    def admin_window(self):
        win = tk.Toplevel(self.root)
        self.set_widget_theme(win)
        win.title("Admin: View All User Bills")
        tk.Label(win, text="Select user to view their bill:", bg=self.bg, fg=self.entry_fg, font=("Arial", 13, "bold")).pack(pady=6)
        user_files = [f for f in os.listdir() if f.endswith("_wishlist.csv")]
        usernames = [f.replace("_wishlist.csv", "") for f in user_files]
        box = tk.Listbox(win, font=("Arial", 12), bg=self.entry_bg, fg=self.entry_fg)
        for u in usernames: box.insert(tk.END, u)
        box.pack(pady=6)
        def view_bill():
            user = box.get(tk.ACTIVE)
            if user: self.show_bill_for_user(user)
        tk.Button(win, text="View Bill", command=view_bill, bg=self.btn_bg, fg="black", font=("Arial", 12)).pack(pady=6)
        tk.Button(win, text="Close", command=win.destroy, bg="#F64C72", fg="black", font=("Arial", 12)).pack(pady=6)

    def show_bill_for_user(self, user):
        filename = f"{user}_wishlist.csv"
        items = []
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 5:
                        items.append((row[0], float(row[1]), int(row[2]), row[3], row[4]))
        except:
            messagebox.showinfo("Bill", f"No items for {user}")
            return

        bill_win = tk.Toplevel(self.root)
        self.set_widget_theme(bill_win)
        bill_win.title(f"{user}'s Wishlist Bill")
        title = tk.Label(bill_win, text=f"{user}'s Wishlist Bill", font=("Arial", 18, "bold"), bg=self.table_bg, fg=self.table_fg)
        title.pack(pady=8)
        columns = ("Item", "Price", "Qty", "Date", "Category", "Cost")
        bill_tree = ttk.Treeview(bill_win, columns=columns, show="headings", height=len(items))
        self.update_tree_style()
        for col in columns:
            bill_tree.heading(col, text=col)
            bill_tree.column(col, anchor="center", width=120)
        for name, price, qty, date, category in items:
            cost = price * qty
            bill_tree.insert('', 'end', values=(name, price, qty, date, category, cost))
        bill_tree.pack(pady=12)

        total = sum(float(price) * int(qty) for name, price, qty, date, category in items)
        costs = [float(price) * int(qty) for name, price, qty, date, category in items]
        summary = f"Total: ₹{total}\nMost expensive: ₹{max(costs) if costs else 0}\nCheapest: ₹{min(costs) if costs else 0}"
        summary_label = tk.Label(bill_win, text=summary, font=("Arial", 13, "bold"), bg=self.table_bg, fg=self.table_fg, justify="left")
        summary_label.pack(pady=4)
        tk.Button(bill_win, text="Close", command=bill_win.destroy, bg="#FFD6E0", fg="#34344A").pack(pady=10)

    def init_main_ui(self):
        tk.Label(self.root, text=f"User: {self.username}", bg=self.bg, fg="#F7CA18", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=6)
        if self.budget:
            tk.Label(self.root, text=f"Budget: ₹{self.budget}", bg=self.bg, fg=self.warning_fg, font=("Arial", 11, "bold")).grid(row=1, column=0, columnspan=6)
        tk.Label(self.root, text="Item Name:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=0)
        self.entry_name = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.entry_name.grid(row=2, column=1)
        tk.Label(self.root, text="Price (₹):", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=2)
        self.entry_price = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.entry_price.grid(row=2, column=3)
        tk.Label(self.root, text="Quantity:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=4)
        self.entry_qty = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.entry_qty.grid(row=2, column=5)
        tk.Label(self.root, text="Date (YYYY/MM/DD):", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=3, column=0)
        self.entry_date = tk.Entry(self.root, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.entry_date.grid(row=3, column=1)
        tk.Label(self.root, text="Category:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=3, column=2)
        self.category_var = tk.StringVar(value=self.CATEGORIES[0])
        self.entry_category = ttk.Combobox(self.root, textvariable=self.category_var, values=self.CATEGORIES, state="readonly", font=("Arial", 12))
        self.entry_category.grid(row=3, column=3)
        tk.Button(self.root, text="Add Item", command=self.add_item, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12)).grid(row=3, column=4, pady=8, columnspan=2)

        tk.Label(self.root, text="Search:", bg=self.bg, fg=self.entry_fg).grid(row=4, column=0)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.root, textvariable=self.search_var, bg=self.entry_bg, fg=self.entry_fg)
        search_entry.grid(row=4, column=1)
        tk.Button(self.root, text="Go", command=self.search_items, bg=self.btn_bg, fg=self.btn_fg).grid(row=4, column=2)
        tk.Button(self.root, text="Show All", command=self.refresh_tree, bg=self.btn_bg, fg=self.btn_fg).grid(row=4, column=3)
        tk.Button(self.root, text="Export CSV", command=self.export_csv, bg="#FFD6E0", fg="#34344A").grid(row=4, column=4)
        tk.Button(self.root, text="Import CSV", command=self.import_csv, bg="#FFD6E0", fg="#34344A").grid(row=4, column=5)
        tk.Button(self.root, text="Show Category Chart", command=self.show_category_chart, bg="#F64C72", fg="black").grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Switch Theme", command=self.toggle_theme, bg=self.btn_bg, fg=self.btn_fg).grid(row=5, column=2)

        self.update_tree_style()
        columns = ("name", "price", "qty", "date", "category")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=7)
        for col in columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, anchor="center", minwidth=60, width=120)
        self.tree.grid(row=6, column=0, columnspan=6, sticky="nsew")
        self.tree.bind("<Double-1>", self.edit_item)
        self.tree.bind("<Button-3>", self.delete_item)
        self.label_total = tk.Label(self.root, text="Total: ₹0", font=("Arial", 14, "bold"), bg=self.bg, fg=self.btn_bg)
        self.label_total.grid(row=7, column=0, columnspan=6)
        tk.Button(self.root, text="Done/Bill", command=self.show_bill_window, bg="#F64C72", fg="black", font=("Arial", 12)).grid(row=8, column=0, columnspan=6)
        self.root.rowconfigure(6, weight=1)
        self.root.columnconfigure(2, weight=1)

    def add_item(self):
        name = self.entry_name.get()
        try:
            price = float(self.entry_price.get())
            qty = int(self.entry_qty.get())
        except:
            messagebox.showerror("Error", "Price must be a number and Quantity an integer.")
            return
    
        date = self.entry_date.get() or get_today_ist()
        category = self.category_var.get()
        self.items.append((name, price, qty, date, category))
        self.save_items()
        self.refresh_tree()
        self.update_total()
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_category.set(self.CATEGORIES[0])


    def edit_item(self, event):
        cur = self.tree.focus()
        idx = self.tree.index(cur)
        if cur:
            item = self.items[idx]
            edit_win = tk.Toplevel(self.root)
            self.set_widget_theme(edit_win)
            edit_win.title("Edit Item")
            tk.Label(edit_win, text="Name:").pack()
            en = tk.Entry(edit_win); en.insert(0, item[0]); en.pack()
            tk.Label(edit_win, text="Price:").pack()
            ep = tk.Entry(edit_win); ep.insert(0, item[1]); ep.pack()
            tk.Label(edit_win, text="Qty:").pack()
            eq = tk.Entry(edit_win); eq.insert(0, item[2]); eq.pack()
            tk.Label(edit_win, text="Date:").pack()
            ed = tk.Entry(edit_win); ed.insert(0, item[3]); ed.pack()
            tk.Label(edit_win, text="Category:").pack()
            ec = ttk.Combobox(edit_win, values=self.CATEGORIES, state="readonly"); ec.set(item[4]); ec.pack()
            def save_edit():
                try:
                    self.items[idx] = (en.get(), float(ep.get()), int(eq.get()), ed.get(), ec.get())
                    self.save_items()
                    self.refresh_tree()
                    self.update_total()
                    edit_win.destroy()
                except:
                    messagebox.showerror("Error", "Invalid inputs.")
            tk.Button(edit_win, text="Save", command=save_edit).pack()

    def delete_item(self, event):
        cur = self.tree.focus()
        idx = self.tree.index(cur)
        if cur and messagebox.askyesno("Delete", "Delete this item?"):
            self.items.pop(idx)
            self.save_items()
            self.refresh_tree()
            self.update_total()

    def load_items(self):
        try:
            with open(self.filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.items = []
                for row in reader:
                    if len(row) == 5:
                        self.items.append((row[0], float(row[1]), int(row[2]), row[3], row[4]))
        except:
            self.items = []

    def save_items(self):
        try:
            with open(self.filename, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for item in self.items:
                    writer.writerow(item)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save: {e}")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for name, price, qty, date, category in self.items:
            self.tree.insert('', 'end', values=(name, price, qty, date, category))

    def update_total(self):
        total = sum(price * qty for _, price, qty, _, _ in self.items)
        txt = f"Total: ₹{total}"
        if self.budget and total > float(self.budget):
            txt += " (Over Budget!)"
            self.label_total.config(fg=self.warning_fg)
        else:
            self.label_total.config(fg=self.btn_bg)
        self.label_total.config(text=txt)

    def show_bill_window(self):
        bill_win = tk.Toplevel(self.root)
        self.set_widget_theme(bill_win)
        bill_win.title(f"{self.username}'s Wishlist Bill")
        title = tk.Label(bill_win, text=f"{self.username}'s Wishlist Bill", font=("Arial", 18, "bold"), bg=self.table_bg, fg=self.table_fg)
        title.pack(pady=8)
        columns = ("Item", "Price", "Qty", "Date", "Category", "Cost")
        bill_tree = ttk.Treeview(bill_win, columns=columns, show="headings", height=len(self.items))
        self.update_tree_style()
        for col in columns:
            bill_tree.heading(col, text=col)
            bill_tree.column(col, anchor="center", width=120)
        for name, price, qty, date, category in self.items:
            cost = price * qty
            bill_tree.insert('', 'end', values=(name, price, qty, date, category, cost))
        bill_tree.pack(pady=12)
        total = sum(price * qty for _, price, qty, _, _ in self.items)
        costs = [price * qty for _, price, qty, _, _ in self.items]
        summary = f"Total: ₹{total}\nMost expensive: ₹{max(costs) if costs else 0}\nCheapest: ₹{min(costs) if costs else 0}"
        summary_label = tk.Label(bill_win, text=summary, font=("Arial", 13, "bold"), bg=self.table_bg, fg=self.table_fg, justify="left")
        summary_label.pack(pady=4)
        tk.Button(bill_win, text="Close", command=bill_win.destroy, bg="#FFD6E0", fg="#34344A").pack(pady=10)

    def sort_by_column(self, col):
        idx = {"name": 0, "price": 1, "qty": 2, "date": 3, "category": 4}[col]
        self.items.sort(key=lambda x: x[idx])
        self.refresh_tree()

    def search_items(self):
        val = self.search_var.get().lower()
        results = []
        for item in self.items:
            if val in item[0].lower() or val in item[4].lower():
                results.append(item)
        self.tree.delete(*self.tree.get_children())
        for name, price, qty, date, category in results:
            self.tree.insert('', 'end', values=(name, price, qty, date, category))

    def export_csv(self):
        fname = filedialog.asksaveasfilename(defaultextension=".csv")
        if fname:
            try:
                with open(fname, "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for item in self.items:
                        writer.writerow(item)
                messagebox.showinfo("Export CSV", "Wishlist exported!")
            except Exception as e:
                messagebox.showerror("Export Error", f"{e}")

    def import_csv(self):
        fname = filedialog.askopenfilename(defaultextension=".csv")
        if fname:
            try:
                with open(fname, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.items = []
                    for row in reader:
                        if len(row) == 5:
                            self.items.append((row[0], float(row[1]), int(row[2]), row[3], row[4]))
                self.save_items()
                self.refresh_tree()
                self.update_total()
                messagebox.showinfo("Import CSV", "Wishlist imported!")
            except Exception as e:
                messagebox.showerror("Import Error", f"{e}")

    def show_category_chart(self):
        cats = {}
        for _, price, qty, _, category in self.items:
            cats[category] = cats.get(category, 0) + price * qty
        if not cats: return
        plt.figure(figsize=(7,5))
        plt.pie(list(cats.values()), labels=list(cats.keys()), autopct='%1.1f%%', startangle=140)
        plt.title("Wishlist Cost Breakdown by Category")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = WishlistAnalyzer(root)
    root.mainloop()
