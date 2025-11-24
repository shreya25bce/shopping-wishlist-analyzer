import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, os, datetime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# simple ist helper
def today_ist():
    tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(tz).strftime("%Y/%m/%d")

class wishapp:
    cats = ["electronics", "books", "groceries", "clothes", "stationery", "other"]

    def __init__(self, master):
        self.r = master
        self.r.title("shopping wishlist cost analyzer")
        self.theme = "dark"
        self.user = None
        self.file = None
        self.items = []
        self.budget = None
        self._set_theme(self.theme)
        self.r.bind("<F2>", lambda e: self.adminwin())
        self.ask_user()

    def _set_theme(self, t):
        if t == "dark":
            self.bg = "#24292f"
            self.entry_bg = "#2d333b"
            self.entry_fg = "#d1d5da"
            self.btn_bg = "#36b37e"
            self.btn_fg = "black"
            self.header_bg = "#36b37e"
            self.header_fg = "black"
            self.table_bg = "#34344a"
            self.table_fg = "#ffd6e0"
            self.warn_fg = "#d6336c"
        else:
            self.bg = "#eaeaea"
            self.entry_bg = "#ffffff"
            self.entry_fg = "#24292f"
            self.btn_bg = "#85c7f2"
            self.btn_fg = "black"
            self.header_bg = "#b2d7ff"
            self.header_fg = "black"
            self.table_bg = "#e5f4f6"
            self.table_fg = "#24292f"
            self.warn_fg = "red"
        try:
            self.r.configure(bg=self.bg)
        except Exception:
            pass

    def _apply_theme_to(self, w):
        for c in w.winfo_children():
            if isinstance(c, (tk.Label, tk.Button, tk.Entry, tk.Toplevel, tk.Frame)):
                try:
                    c.configure(bg=self.bg, fg=self.entry_fg)
                except Exception:
                    pass

    def ask_user(self):
        w = tk.Toplevel(self.r)
        self._apply_theme_to(w)
        w.title("enter username")
        tk.Label(w, text="enter username (or admin):", bg=self.bg, fg=self.entry_fg).pack(pady=6)
        e = tk.Entry(w, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        e.pack(pady=6)
        tk.Label(w, text="enter budget (optional):", bg=self.bg, fg=self.entry_fg).pack()
        be = tk.Entry(w, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        be.pack()

        def dop():
            name = e.get().strip()
            self.budget = be.get().strip()
            if not name:
                messagebox.showerror("error", "please enter a username.")
                return
            if name.lower() == "admin":
                w.destroy()
                self.adminwin()
            else:
                self.user = name
                self.file = f"{self.user}_wishlist.csv"
                w.destroy()
                self.build_ui()
                self.load()
                self.refr()
                self.upd_total()

        tk.Button(w, text="done", command=dop, bg="#f64c72", fg="black").pack(pady=8)

    def toggle(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self._set_theme(self.theme)
        for wid in self.r.winfo_children():
            if isinstance(wid, (tk.Label, tk.Button, tk.Entry, tk.Toplevel, tk.Frame)):
                try:
                    wid.configure(bg=self.bg, fg=self.entry_fg)
                except Exception:
                    pass
        self._style_tree()
        self.refr()

    def _style_tree(self):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("Treeview", background=self.table_bg, fieldbackground=self.table_bg,
                    foreground=self.table_fg, rowheight=28, bordercolor=self.btn_bg, borderwidth=1)
        s.configure("Treeview.Heading", background=self.header_bg, foreground=self.header_fg, font=("Arial", 11, "bold"))
        s.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        s.map("Treeview", background=[("selected", self.entry_bg)])

    def adminwin(self):
        w = tk.Toplevel(self.r)
        self._apply_theme_to(w)
        w.title("admin: view all user bills")
        tk.Label(w, text="select user to view their bill:", bg=self.bg, fg=self.entry_fg, font=("Arial", 13, "bold")).pack(pady=6)
        files = [f for f in os.listdir() if f.endswith("_wishlist.csv")]
        users = [f.replace("_wishlist.csv", "") for f in files]
        lb = tk.Listbox(w, font=("Arial", 12), bg=self.entry_bg, fg=self.entry_fg)
        for u in users:
            lb.insert(tk.END, u)
        lb.pack(pady=6)

        def vb():
            try:
                user = lb.get(tk.ACTIVE)
            except Exception:
                user = None
            if user:
                self.show_bill_user(user)

        tk.Button(w, text="view bill", command=vb, bg=self.btn_bg, fg="black", font=("Arial", 12)).pack(pady=6)
        tk.Button(w, text="close", command=w.destroy, bg="#f64c72", fg="black", font=("Arial", 12)).pack(pady=6)

    def show_bill_user(self, user):
        fn = f"{user}_wishlist.csv"
        its = []
        try:
            with open(fn, newline='', encoding='utf-8') as f:
                rd = csv.reader(f)
                for r in rd:
                    if len(r) == 5:
                        its.append((r[0], float(r[1]), int(r[2]), r[3], r[4]))
        except Exception:
            messagebox.showinfo("bill", f"no items for {user}")
            return

        bw = tk.Toplevel(self.r)
        self._apply_theme_to(bw)
        bw.title(f"{user}'s wishlist bill")
        tk.Label(bw, text=f"{user}'s wishlist bill", font=("Arial", 18, "bold"), bg=self.table_bg, fg=self.table_fg).pack(pady=8)
        cols = ("item", "price", "qty", "date", "category", "cost")
        tr = ttk.Treeview(bw, columns=cols, show="headings", height=len(its))
        self._style_tree()
        for c in cols:
            tr.heading(c, text=c)
            tr.column(c, anchor="center", width=120)
        for n, p, q, d, cat in its:
            cost = p * q
            tr.insert('', 'end', values=(n, p, q, d, cat, cost))
        tr.pack(pady=12)

        total = sum(float(p) * int(q) for n, p, q, d, cat in its)
        costs = [float(p) * int(q) for n, p, q, d, cat in its]
        summ = f"total: ₹{total}\nmost expensive: ₹{max(costs) if costs else 0}\ncheapest: ₹{min(costs) if costs else 0}"
        tk.Label(bw, text=summ, font=("Arial", 13, "bold"), bg=self.table_bg, fg=self.table_fg, justify="left").pack(pady=4)
        tk.Button(bw, text="close", command=bw.destroy, bg="#ffd6e0", fg="#34344a").pack(pady=10)

    def build_ui(self):
        tk.Label(self.r, text=f"user: {self.user}", bg=self.bg, fg="#f7ca18", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=6)
        if self.budget:
            tk.Label(self.r, text=f"budget: ₹{self.budget}", bg=self.bg, fg=self.warn_fg, font=("Arial", 11, "bold")).grid(row=1, column=0, columnspan=6)

        tk.Label(self.r, text="item name:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=0)
        self.e_name = tk.Entry(self.r, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.e_name.grid(row=2, column=1)

        tk.Label(self.r, text="price (₹):", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=2)
        self.e_price = tk.Entry(self.r, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.e_price.grid(row=2, column=3)

        tk.Label(self.r, text="quantity:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=2, column=4)
        self.e_qty = tk.Entry(self.r, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.e_qty.grid(row=2, column=5)

        tk.Label(self.r, text="date (yyyy/mm/dd):", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=3, column=0)
        self.e_date = tk.Entry(self.r, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Arial", 12))
        self.e_date.grid(row=3, column=1)

        tk.Label(self.r, text="category:", bg=self.bg, fg=self.entry_fg, font=("Arial", 12)).grid(row=3, column=2)
        self.catvar = tk.StringVar(value=self.cats[0])
        self.e_cat = ttk.Combobox(self.r, textvariable=self.catvar, values=self.cats, state="readonly", font=("Arial", 12))
        self.e_cat.grid(row=3, column=3)

        tk.Button(self.r, text="add item", command=self.add_item, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12)).grid(row=3, column=4, pady=8, columnspan=2)

        tk.Label(self.r, text="search:", bg=self.bg, fg=self.entry_fg).grid(row=4, column=0)
        self.svar = tk.StringVar()
        se = tk.Entry(self.r, textvariable=self.svar, bg=self.entry_bg, fg=self.entry_fg)
        se.grid(row=4, column=1)
        tk.Button(self.r, text="go", command=self.search, bg=self.btn_bg, fg=self.btn_fg).grid(row=4, column=2)
        tk.Button(self.r, text="show all", command=self.refr, bg=self.btn_bg, fg=self.btn_fg).grid(row=4, column=3)
        tk.Button(self.r, text="export csv", command=self.export_csv, bg="#ffd6e0", fg="#34344a").grid(row=4, column=4)
        tk.Button(self.r, text="import csv", command=self.import_csv, bg="#ffd6e0", fg="#34344a").grid(row=4, column=5)
        tk.Button(self.r, text="show category chart", command=self.cat_chart, bg="#f64c72", fg="black").grid(row=5, column=0, columnspan=2)
        tk.Button(self.r, text="switch theme", command=self.toggle, bg=self.btn_bg, fg=self.btn_fg).grid(row=5, column=2)

        self._style_tree()
        cols = ("name", "price", "qty", "date", "category")
        self.tr = ttk.Treeview(self.r, columns=cols, show="headings", height=7)
        for c in cols:
            self.tr.heading(c, text=c, command=lambda cc=c: self.sort_by(cc))
            self.tr.column(c, anchor="center", minwidth=60, width=120)
        self.tr.grid(row=6, column=0, columnspan=6, sticky="nsew")
        self.tr.bind("<Double-1>", self.edit)
        self.tr.bind("<Button-3>", self.delete)
        self.lbl_tot = tk.Label(self.r, text="total: ₹0", font=("Arial", 14, "bold"), bg=self.bg, fg=self.btn_bg)
        self.lbl_tot.grid(row=7, column=0, columnspan=6)
        tk.Button(self.r, text="done/bill", command=self.billwin, bg="#f64c72", fg="black", font=("Arial", 12)).grid(row=8, column=0, columnspan=6)
        self.r.rowconfigure(6, weight=1)
        self.r.columnconfigure(2, weight=1)

    def add_item(self):
        name = self.e_name.get()
        try:
            price = float(self.e_price.get())
            qty = int(self.e_qty.get())
        except Exception:
            messagebox.showerror("error", "price must be a number and quantity an integer.")
            return
        date = self.e_date.get() or today_ist()
        cat = self.catvar.get()
        self.items.append((name, price, qty, date, cat))
        self.save()
        self.refr()
        self.upd_total()
        self.e_name.delete(0, tk.END)
        self.e_price.delete(0, tk.END)
        self.e_qty.delete(0, tk.END)
        self.e_date.delete(0, tk.END)
        self.e_cat.set(self.cats[0])

    def edit(self, ev):
        cur = self.tr.focus()
        idx = self.tr.index(cur)
        if cur:
            it = self.items[idx]
            ew = tk.Toplevel(self.r)
            self._apply_theme_to(ew)
            ew.title("edit item")
            tk.Label(ew, text="name:").pack()
            en = tk.Entry(ew); en.insert(0, it[0]); en.pack()
            tk.Label(ew, text="price:").pack()
            ep = tk.Entry(ew); ep.insert(0, it[1]); ep.pack()
            tk.Label(ew, text="qty:").pack()
            eq = tk.Entry(ew); eq.insert(0, it[2]); eq.pack()
            tk.Label(ew, text="date:").pack()
            ed = tk.Entry(ew); ed.insert(0, it[3]); ed.pack()
            tk.Label(ew, text="category:").pack()
            ec = ttk.Combobox(ew, values=self.cats, state="readonly"); ec.set(it[4]); ec.pack()

            def save_ed():
                try:
                    self.items[idx] = (en.get(), float(ep.get()), int(eq.get()), ed.get(), ec.get())
                    self.save()
                    self.refr()
                    self.upd_total()
                    ew.destroy()
                except Exception:
                    messagebox.showerror("error", "invalid inputs.")
            tk.Button(ew, text="save", command=save_ed).pack()

    def delete(self, ev):
        cur = self.tr.focus()
        idx = self.tr.index(cur)
        if cur and messagebox.askyesno("delete", "delete this item?"):
            self.items.pop(idx)
            self.save()
            self.refr()
            self.upd_total()

    def load(self):
        try:
            with open(self.file, newline='', encoding='utf-8') as f:
                rd = csv.reader(f)
                self.items = []
                for r in rd:
                    if len(r) == 5:
                        self.items.append((r[0], float(r[1]), int(r[2]), r[3], r[4]))
        except Exception:
            self.items = []

    def save(self):
        try:
            with open(self.file, "w", newline='', encoding='utf-8') as f:
                wr = csv.writer(f)
                for it in self.items:
                    wr.writerow(it)
        except Exception as e:
            messagebox.showerror("file error", f"could not save: {e}")

    def refr(self):
        for x in self.tr.get_children():
            self.tr.delete(x)
        for n, p, q, d, c in self.items:
            self.tr.insert('', 'end', values=(n, p, q, d, c))

    def upd_total(self):
        total = sum(p * q for _, p, q, _, _ in self.items)
        txt = f"total: ₹{total}"
        if self.budget:
            try:
                if total > float(self.budget):
                    txt += " (over budget!)"
                    self.lbl_tot.config(fg=self.warn_fg)
                else:
                    self.lbl_tot.config(fg=self.btn_bg)
            except Exception:
                # invalid budget input - ignore coloring
                self.lbl_tot.config(fg=self.btn_bg)
        else:
            self.lbl_tot.config(fg=self.btn_bg)
        self.lbl_tot.config(text=txt)

    def billwin(self):
        bw = tk.Toplevel(self.r)
        self._apply_theme_to(bw)
        bw.title(f"{self.user}'s wishlist bill")
        tk.Label(bw, text=f"{self.user}'s wishlist bill", font=("Arial", 18, "bold"), bg=self.table_bg, fg=self.table_fg).pack(pady=8)
        cols = ("item", "price", "qty", "date", "category", "cost")
        tr = ttk.Treeview(bw, columns=cols, show="headings", height=len(self.items))
        self._style_tree()
        for c in cols:
            tr.heading(c, text=c)
            tr.column(c, anchor="center", width=120)
        for n, p, q, d, cat in self.items:
            cost = p * q
            tr.insert('', 'end', values=(n, p, q, d, cat, cost))
        tr.pack(pady=12)
        total = sum(p * q for _, p, q, _, _ in self.items)
        costs = [p * q for _, p, q, _, _ in self.items]
        summ = f"total: ₹{total}\nmost expensive: ₹{max(costs) if costs else 0}\ncheapest: ₹{min(costs) if costs else 0}"
        tk.Label(bw, text=summ, font=("Arial", 13, "bold"), bg=self.table_bg, fg=self.table_fg, justify="left").pack(pady=4)
        tk.Button(bw, text="close", command=bw.destroy, bg="#ffd6e0", fg="#34344a").pack(pady=10)

    def sort_by(self, col):
        idx = {"name": 0, "price": 1, "qty": 2, "date": 3, "category": 4}[col]
        try:
            self.items.sort(key=lambda x: x[idx])
        except Exception:
            pass
        self.refr()

    def search(self):
        v = self.svar.get().lower()
        res = []
        for it in self.items:
            if v in (it[0] or "").lower() or v in (it[4] or "").lower():
                res.append(it)
        self.tr.delete(*self.tr.get_children())
        for n, p, q, d, c in res:
            self.tr.insert('', 'end', values=(n, p, q, d, c))

    def export_csv(self):
        fn = filedialog.asksaveasfilename(defaultextension=".csv")
        if fn:
            try:
                with open(fn, "w", newline='', encoding='utf-8') as f:
                    wr = csv.writer(f)
                    for it in self.items:
                        wr.writerow(it)
                messagebox.showinfo("export csv", "wishlist exported!")
            except Exception as e:
                messagebox.showerror("export error", f"{e}")

    def import_csv(self):
        fn = filedialog.askopenfilename(defaultextension=".csv")
        if fn:
            try:
                with open(fn, newline='', encoding='utf-8') as f:
                    rd = csv.reader(f)
                    self.items = []
                    for r in rd:
                        if len(r) == 5:
                            self.items.append((r[0], float(r[1]), int(r[2]), r[3], r[4]))
                self.save()
                self.refr()
                self.upd_total()
                messagebox.showinfo("import csv", "wishlist imported!")
            except Exception as e:
                messagebox.showerror("import error", f"{e}")

    def cat_chart(self):
        catmap = {}
        for _, p, q, _, cat in self.items:
            catmap[cat] = catmap.get(cat, 0) + p * q
        if not catmap:
            return
        plt.figure(figsize=(7,5))
        plt.pie(list(catmap.values()), labels=list(catmap.keys()), autopct='%1.1f%%', startangle=140)
        plt.title("wishlist cost breakdown by category")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = wishapp(root)
    root.mainloop()
