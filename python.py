import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, os, datetime
import matplotlib.pyplot as plt

from datetime import datetime, timedelta, timezone

def get_today_ist():
    # IST is UTC+5:30
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
