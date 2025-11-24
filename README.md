# Shopping Wishlist Cost Analyzer

## Overview
This is a Python Tkinter app to manage and analyze personal shopping wishlists with features for having a budget, category analysis, multi-user mode, and an admin mode. This project is built for VIT Bhopal VITyarthi project submission.

## Features
- **Multi-user support:** every user has their own wishlist file in a csv format
- **Admin mode:** if we type 'admin' at login, we can view all users' consolidated bills
- **Item management:** add, edit, delete wishlist items with name, price, quantity, date, and category
- **Category analytics:** a piechart showing cost breakdown by category 
- **Budget tracking:** enter your budget and receive alerts if wishlist exceeds it by also using color-code changes
- **Automatic IST date:** this auto fills today's date (IST) if left blank when adding items
- **Search & filter:** to search items by name or category
- **Sortable table:** click column headers to sort by any field
- **Import/Export CSV:** save and load wishlists from csv files for data backup or sharing
- **Dark/Light theme:** to toggle between themes
- **User-friendly UI:** it uses a clean Tkinter interface with color-coded warnings and buttons

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shreya25bce/shopping-wishlist-analyzer.git
   cd shopping-wishlist-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install matplotlib
   ```

3. **Run the app:**
   ```bash
   python python.py
   ```
   Or in IDLE: File → Open → select `python.py` → Run Module

### Usage Guide

1. **Login:** enter your username and optional budget if any
2. **Add items:** fill in item details and click "add item" to commit
3. **View bill:** click on "done" to see your complete wishlist bill after
4. **Analyze:** click "show category chart" for a piechart breakdown
5. **Admin access:** type 'admin' to view all users' bills in the admin mode
6. **Import/Export:** use the buttons given to save or load CSV data
7. **Theme:** switch between dark and light modes anytime

## Sample CSV Format

Place a CSV file in the same directory with format:
```
item name,price,quantity,date,category
Laptop,65000,1,2025/11/23,Electronics
Python Book,700,2,2025/11/20,Books
Water Bottle,250,3,2025/11/19,Groceries
T-Shirt,500,2,2025/11/18,Clothes
Notebook,80,5,2025/11/22,Stationery
Backpack,1800,1,2025/11/22,Other
```

## File Structure
```
shopping-wishlist-analyzer/
├── python.py              # the main application file
├── README.md              # this file
├── {username}_wishlist.csv # auto-generated user files
└── /screenshots/          # the project's screenshots 
```

## Project Features (Technical)

### Core Functionality
- **OOP Design:** single `WishlistAnalyzer` class managing all operations
- **CSV data persistence:** automatic save/load of user wishlists
- **Error handling:** exception handling for file I/O and user input
- **IST timezone support:** auto-date uses Indian Standard Time
- **Matplotlib integration:** dynamic pie chart generation

### UI Components
- **Tkinter widgets:** labels, entry fields, buttons, treeview table, combobox dropdown
- **Theme system:** dynamic color scheme switching with safe widget updates
- **Multi-window support:** main window + popup dialogs for editing, bills, admin views

## Keyboard Shortcuts
- **F2:** open admin mode
- **Double-click item:** edit item
- **Right-click item:** delete item

## Requirements Met
✅ multi-user wishlist management  
✅ category wise cost analytics like a piechart 
✅ tracking on budget with warnings  
✅ admin mode to view all users' and their respective bills 
✅ add/edit/delete/search items  
✅ import/export csv   
✅ ist date auto-fill  
✅ dark/light theme toggle  
✅ error handling  

## Credits
- **Student:** Shreya Arora
- **Registration:** 25bce10621
- **Institution:** Vellore Institute of Technology, Bhopal
- **Course:** VITyarthi Project Submission
- **Date:** November 2025

## License
MIT License - Free to use for educational and personal purposes.

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'matplotlib'"**
- Run: `pip install matplotlib` in your terminal

**"_tkinter.TclError: unknown option \"-bg\""**
- This has been fixed in the current version. Update your code.

**CSV file not loading**
- Ensure CSV format matches the sample (5 columns, correct order)
- Check file is in the same directory as the script
- Try using "Import CSV" button instead

**App won't run in IDLE**
- Make sure you installed matplotlib for the correct Python version
- In IDLE: Python Launcher → Check Python version matches 3.10+

## Support
For issues or questions, please refer to the code comments or create an issue on GitHub.
