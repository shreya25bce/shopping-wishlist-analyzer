# Shopping Wishlist Cost Analyzer

## Overview
A Python Tkinter app to manage and analyze personal shopping wishlists, with features for budgeting, category analytics, multi-user mode, and admin bill viewing. Built for VIT Bhopal VITyarthi project submission.

## Features
- **Multi-user support:** Each user has their own wishlist file (CSV format)
- **Admin mode:** Type 'admin' at login (or press F2) to view all users' consolidated bills
- **Item management:** Add, edit, delete wishlist items with name, price, quantity, date, and category
- **Category analytics:** Pie chart showing cost breakdown by category (Electronics, Books, Groceries, Clothes, Stationery, Other)
- **Budget tracking:** Enter your target budget and receive alerts if wishlist exceeds it
- **Automatic IST date:** Auto-fills today's date (IST) if left blank when adding items
- **Search & filter:** Search items by name or category
- **Sortable table:** Click column headers to sort by any field
- **Import/Export CSV:** Save and load wishlists from CSV files for data backup or sharing
- **Dark/Light theme:** Toggle between themes without crashes, with robust error handling
- **User-friendly UI:** Clean Tkinter interface with color-coded warnings and intuitive buttons

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

1. **Login:** Enter your username and optional budget
2. **Add items:** Fill in item details and click "Add Item"
3. **View bill:** Click "Done/Bill" to see your complete wishlist bill
4. **Analyze:** Click "Show Category Chart" for a pie chart breakdown
5. **Admin access:** Type 'admin' to view all users' bills
6. **Import/Export:** Use buttons to save or load CSV data
7. **Theme:** Switch between dark and light modes anytime

## Sample CSV Format

Place a CSV file in the same directory with format:
```
Item Name,Price,Quantity,Date,Category
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
├── python.py              # Main application file
├── README.md              # This file
├── {username}_wishlist.csv # Auto-generated user files
└── /screenshots/          # Project screenshots (for documentation)
```

## Project Features (Technical)

### Core Functionality
- **OOP Design:** Single `WishlistAnalyzer` class managing all operations
- **CSV data persistence:** Automatic save/load of user wishlists
- **Error handling:** Robust exception handling for file I/O and user input
- **IST timezone support:** Auto-date uses Indian Standard Time
- **Matplotlib integration:** Dynamic pie chart generation

### UI Components
- **Tkinter widgets:** Labels, Entry fields, Buttons, Treeview (table), Combobox (dropdown)
- **Theme system:** Dynamic color scheme switching with safe widget updates
- **Multi-window support:** Main window + popup dialogs for editing, bills, admin views

## Keyboard Shortcuts
- **F2:** Open admin mode
- **Double-click item:** Edit item
- **Right-click item:** Delete item

## Requirements Met
✅ Multi-user wishlist management  
✅ Category-wise cost analytics (pie chart)  
✅ Budget tracking with warnings  
✅ Admin panel to view all users  
✅ Add/Edit/Delete/Search items  
✅ Import/Export CSV functionality  
✅ IST date auto-fill  
✅ Dark/Light theme toggle  
✅ Robust error handling  
✅ Original Python code (no AI generation)  

## Credits
- **Student:** Shreya Arora
- **Registration:** 10621
- **VIT ID:** shreya25bce
- **Institution:** VIT Bhopal
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
