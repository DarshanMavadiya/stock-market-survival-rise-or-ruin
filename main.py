import tkinter as tk
from popup_style import *
import random
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from popup_style import *
from ui_buttons import create_button

# Starting game values
cash = 100000
day = 1

# Player name
player_name = ""

# ----------------------------
# Difficulty Level
# ----------------------------

difficulty = "Normal"

# ----------------------------
# Game Data
# ----------------------------

stocks = {
    "TECH": 100,
    "BANK": 100,
    "AI": 100,
    "ENERGY": 100,
    "PHARMA": 100,
    "CRYPTO": 100
}

# ----------------------------
# Stock Price History
# ----------------------------

price_history = {
    "TECH": [100],
    "BANK": [100],
    "AI": [100],
    "ENERGY": [100],
    "PHARMA": [100],
    "CRYPTO": [100]
}

# Store previous day's prices
previous_prices = stocks.copy()

portfolio = {
    "TECH": 0,
    "BANK": 0,
    "AI": 0,
    "ENERGY": 0,
    "PHARMA": 0,
    "CRYPTO": 0
}

average_buy_price = {
    "TECH": 0,
    "BANK": 0,
    "AI": 0,
    "ENERGY": 0,
    "PHARMA": 0,
    "CRYPTO": 0
}

# ----------------------------
# Stock Split Tracking
# ----------------------------

last_split_day = {
    "TECH": 0,
    "BANK": 0,
    "AI": 0,
    "ENERGY": 0,
    "PHARMA": 0,
    "CRYPTO": 0
}

# ----------------------------
# Achievement Tracking
# ----------------------------

achievements_unlocked = set()

# ----------------------------
# Statistics
# ----------------------------

buy_trades = 0
sell_trades = 0
best_net_worth = 100000

# ----------------------------
# Game State
# ----------------------------

# Prevents game logic from running after the game ends.
game_over = False

# ----------------------------
# Transaction History
# ----------------------------

# Stores all buy/sell trades
# Used by History button
# Saved in savegame.json
transaction_history = []

# ----------------------------
# Main Window
# ----------------------------

root = tk.Tk()

# ----------------------------
# Player Name
# ----------------------------

player_name = tk.simpledialog.askstring(
    "Player Name",
    "Enter your name:"
)

if not player_name:
    player_name = "Player"

# ----------------------------
# Select Difficulty
# ----------------------------

difficulty = simpledialog.askstring(
    "Difficulty",
    "Choose: Easy, Normal, Hard"
)

if difficulty not in ["Easy", "Normal", "Hard"]:
    difficulty = "Normal"

# ----------------------------
# Starting Cash By Difficulty
# ----------------------------

if difficulty == "Easy":
    cash = 150000

elif difficulty == "Hard":
    cash = 75000

else:
    cash = 100000

best_net_worth = cash

# Window title
root.title("Stock Market Survival: Rise or Ruin")

# Start maximized
root.state("zoomed")

# Center window
root.update_idletasks()

width = 1400
height = 900

x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)

root.geometry(f"{width}x{height}+{x}+{y}")

# Prevent layout from collapsing on smaller screens
root.minsize(1600, 900)

# Dark background
root.configure(bg="#0f172a")

# ----------------------------
# Header
# ----------------------------

header_frame = tk.Frame(
    root,
    bg="#0f172a"
)

header_frame.pack(
    fill="x",
    padx=12,
    pady=(12, 8)
)

header_frame.grid_columnconfigure(0, weight=0)
header_frame.grid_columnconfigure(1, weight=1)

# ----------------------------
# Title Container
# ----------------------------

title_frame = tk.Frame(
    header_frame,
    bg="#0f172a"
)

title_frame.grid(
    row=0,
    column=0,
    sticky="nw",
    padx=(0, 18)
)

title_label = tk.Label(
    title_frame,
    text="STOCK MARKET SURVIVAL",
    font=("Segoe UI", 20, "bold"),
    fg="#F8FAFC",
    bg="#0f172a"
)

title_label.pack(anchor="w")

subtitle_label = tk.Label(
    title_frame,
    text="RISE OR RUIN",
    font=("Segoe UI", 13, "bold"),
    fg="#F97316",
    bg="#0f172a"
)

subtitle_label.pack(anchor="w")

# ----------------------------
# Dashboard Cards Container
# ----------------------------

stats_frame = tk.Frame(
    header_frame,
    bg="#0f172a"
)

stats_frame.grid(
    row=0,
    column=1,
    sticky="ew"
)

# Make cards spread evenly
for col in range(6):
    stats_frame.grid_columnconfigure(
        col,
        weight=1
    )

# ----------------------------
# Dashboard Card Helper
# ----------------------------

def create_dashboard_card(
    parent,
    title,
    value,
    title_color,
    value_color
):
    """
    Creates a modern dashboard card.
    UI only - no game logic.
    """

    card = tk.Frame(
        parent,
        bg="#182235",
        highlightbackground=title_color,
        highlightthickness=2,
        bd=0,
        height=78
    )

    card.pack_propagate(False)

    # Top accent line
    tk.Frame(
        card,
        bg=title_color,
        height=3
    ).pack(fill="x")

    title_label = tk.Label(
        card,
        text=title,
        font=("Segoe UI", 9, "bold"),
        fg=title_color,
        bg="#182235"
    )

    title_label.pack(
        anchor="w",
        padx=10,
        pady=(6, 1)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Segoe UI", 13, "bold"),
        fg=value_color,
        bg="#182235"
    )

    value_label.pack(
        anchor="w",
        padx=10,
        pady=(0, 6)
    )

    return card, value_label

# Allow maximize and resizing
root.resizable(True, True)

# ----------------------------
# Dashboard Cards
# ----------------------------

day_card, day_label = create_dashboard_card(
    stats_frame,
    "DAY",
    "Day 1 / 30",
    "#94a3b8",
    "white"
)

day_card.grid(
    row=0,
    column=0,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

cash_card, cash_label = create_dashboard_card(
    stats_frame,
    "CASH",
    f"₹{cash:,}",
    "#22c55e",
    "#22c55e"
)

cash_card.grid(
    row=0,
    column=1,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

net_card, net_worth_label = create_dashboard_card(
    stats_frame,
    "NET WORTH",
    f"₹{cash:,}",
    "#facc15",
    "#facc15"
)

net_card.grid(
    row=0,
    column=2,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

portfolio_card, portfolio_value_label = create_dashboard_card(
    stats_frame,
    "PORTFOLIO",
    "₹0",
    "#38bdf8",
    "#38bdf8"
)

portfolio_card.grid(
    row=0,
    column=3,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

profit_card, profit_loss_label = create_dashboard_card(
    stats_frame,
    "PROFIT / LOSS",
    "₹0",
    "white",
    "white"
)

profit_card.grid(
    row=0,
    column=4,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

difficulty_card, difficulty_label = create_dashboard_card(
    stats_frame,
    "DIFFICULTY",
    difficulty,
    "#f97316",
    "#f97316"
)

difficulty_card.grid(
    row=0,
    column=5,
    padx=(3, 3),
    pady=(2, 2),
    sticky="nsew"
)

# ----------------------------
# Main Content Frame
# ----------------------------

content_frame = tk.Frame(
    root,
    bg="#0f172a"
)

content_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(0, 12)
)

# Responsive columns
# Responsive dashboard columns
content_frame.grid_columnconfigure(
    0,
    weight=3
)

content_frame.grid_columnconfigure(
    1,
    weight=2
)

content_frame.grid_columnconfigure(
    2,
    weight=3
)

content_frame.grid_columnconfigure(
    3,
    weight=0
)

# Make rows resize with window
content_frame.grid_rowconfigure(
    0,
    weight=0,
    minsize=250
)

content_frame.grid_rowconfigure(
    1,
    weight=1
)

content_frame.grid_rowconfigure(
    2,
    weight=0,
    minsize=110
)

# ----------------------------
# Market Panel
# ----------------------------

market_frame = tk.LabelFrame(
    content_frame,
    text="Market Overview",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b",
    height=260
)

market_frame.grid(
    row=0,
    column=0,
    padx=(0, 6),
    pady=(0, 6),
    sticky="nsew"
)

market_frame.grid_propagate(False)

market_frame.grid_rowconfigure(
    0,
    weight=1
)

market_frame.grid_columnconfigure(
    0,
    weight=1
)

table_style = ttk.Style()

table_style.map(
    "Treeview",
    background=[("selected", "#2563eb")],
    foreground=[("selected", "white")]
)

# Disable heading hover/pressed effect
table_style.layout(
    "Treeview.Heading",
    [
        (
            "Treeheading.cell",
            {
                "sticky": "nswe",
                "children": [
                    (
                        "Treeheading.border",
                        {
                            "sticky": "nswe",
                            "children": [
                                (
                                    "Treeheading.padding",
                                    {
                                        "sticky": "nswe",
                                        "children": [
                                            (
                                                "Treeheading.image",
                                                {"side": "right", "sticky": ""}
                                            ),
                                            (
                                                "Treeheading.text",
                                                {"sticky": "we"}
                                            )
                                        ]
                                    }
                                )
                            ]
                        }
                    )
                ]
            }
        )
    ]
)

# Use clam theme so custom Treeview colors work correctly
table_style.theme_use("clam")

table_style.configure(
    "Treeview",
    background="#162033",
    foreground="white",
    fieldbackground="#162033",
    borderwidth=0,
    rowheight=28,
    font=("Segoe UI", 11)
)

table_style.configure(
    "Treeview.Heading",
    background="#0b3b74",
    foreground="white",
    relief="flat",
    borderwidth=0,
    padding=(6, 8),
    font=("Segoe UI", 11, "bold")
)

# ----------------------------
# Market Overview Table
# ----------------------------

market_tree = ttk.Treeview(
    market_frame,
    columns=(
        "Stock",
        "Price",
        "Movement"
    ),
    show="headings",
    height=6
)

market_tree.heading(
    "Stock",
    text="Stock"
)

market_tree.heading(
    "Price",
    text="Price"
)

market_tree.heading(
    "Movement",
    text="Movement"
)

market_tree.column(
    "Stock",
    width=95,
    anchor="center"
)

market_tree.column(
    "Price",
    width=85,
    anchor="center"
)

market_tree.column(
    "Movement",
    width=210,
    anchor="center"
)

market_tree.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(10, 10)
)

# Market table row colors

market_tree.tag_configure(
    "gain",
    foreground="#22c55e",
    background="#10261a"
)

market_tree.tag_configure(
    "loss",
    foreground="#ef4444",
    background="#2a1313"
)

market_tree.tag_configure(
    "neutral",
    foreground="white",
    background="#1e293b"
)

# ----------------------------
# Populate Market Table
# ----------------------------

for stock in stocks:

    market_tree.insert(
        "",
        "end",
        iid=stock,
        values=(
            stock,
            f"₹{stocks[stock]}",
            "₹0 (0.00%) →"
        )
    )

# ----------------------------
# Portfolio Panel
# ----------------------------

portfolio_frame = tk.LabelFrame(
    content_frame,
    text="Portfolio",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b",
    height=260
)

portfolio_frame.grid(
    row=0,
    column=1,
    padx=6,
    pady=(0, 6),
    sticky="nsew"
)

portfolio_frame.grid_propagate(False)

portfolio_frame.grid_rowconfigure(
    0,
    weight=1
)

portfolio_frame.grid_columnconfigure(
    0,
    weight=1
)

# ----------------------------
# Portfolio Table
# ----------------------------

portfolio_tree = ttk.Treeview(
    portfolio_frame,
    columns=(
        "Stock",
        "Shares",
        "AvgPrice",
        "CurrentPrice",
        "Value",
        "PL"
    ),
    show="headings",
    height=6
)

portfolio_tree.heading(
    "Stock",
    text="Stock",
)

portfolio_tree.heading(
    "Shares",
    text="Shares"
)

portfolio_tree.heading(
    "AvgPrice",
    text="Avg"
)

portfolio_tree.heading(
    "CurrentPrice",
    text="Current"
)

portfolio_tree.heading(
    "Value",
    text="Value"
)

portfolio_tree.heading(
    "PL",
    text="P/L"
)

portfolio_tree.column(
    "Stock",
    width=85,
    anchor="center"
)

portfolio_tree.column(
    "Shares",
    width=75,
    anchor="center"
)

portfolio_tree.column(
    "AvgPrice",
    width=95,
    anchor="center"
)

portfolio_tree.column(
    "CurrentPrice",
    width=95,
    anchor="center"
)

portfolio_tree.column(
    "Value",
    width=105,
    anchor="center"
)

portfolio_tree.column(
    "PL",
    width=120,
    anchor="center"
)

portfolio_tree.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(10, 10)
)

for stock in portfolio:

    portfolio_tree.insert(
        "",
        "end",
        iid=stock,
        values=(
            stock,
            0,
            "₹0",
            f"₹{stocks[stock]:,.0f}",
            "₹0",
            "₹0"
        )
    )

# Portfolio row colors
portfolio_tree.tag_configure(
    "profit",
    foreground="#22c55e"
)

portfolio_tree.tag_configure(
    "loss",
    foreground="#ef4444"
)

portfolio_tree.tag_configure(
    "neutral",
    foreground="white"
)

# ----------------------------
# Market News Events
# ----------------------------

news_events = [
    (
        "AI Boom!",
        "AI",
        20,
        "Investors rush into AI companies."
    ),

    (
        "Bank Crisis!",
        "BANK",
        -20,
        "Major lenders report heavy losses."
    ),

    (
        "Tech Breakthrough!",
        "TECH",
        20,
        "A revolutionary technology is announced."
    ),

    (
        "Energy Shortage!",
        "ENERGY",
        20,
        "Global energy supply tightens."
    ),

    (
        "Pharma Breakthrough!",
        "PHARMA",
        20,
        "A major drug receives regulatory approval."
    ),

    (
        "Crypto Rally!",
        "CRYPTO",
        25,
        "Digital assets surge on investor optimism."
    ),

    (
        "Crypto Crash!",
        "CRYPTO",
        -25,
        "Cryptocurrency markets experience heavy selling."
    ),

    (
        "Market Correction!",
        "ALL",
        -10,
        "Investors take profits after a rally."
    ),

    (
        "Economic Growth!",
        "ALL",
        10,
        "Strong economic data boosts confidence."
    )
]

# ----------------------------
# News History
# Initially empty
# ----------------------------

news_history = []

# ----------------------------
# Special Market Events
# ----------------------------

special_events = [
    ("AI Revolution!", "AI", 50),
    ("Banking Crash!", "BANK", -50),
    ("Energy Crisis!", "ENERGY", 50),
    ("Tech Bubble Burst!", "TECH", -50),
    ("Pharma Miracle Drug!", "PHARMA", 50),
    ("Crypto Meltdown!", "CRYPTO", -50),
    ("Bull Run!", "ALL", 30),
    ("Market Panic!", "ALL", -30)
]

# ----------------------------
# Dividend Events
# ----------------------------

dividend_events = [
    ("TECH", 5),
    ("BANK", 4),
    ("AI", 6),
    ("ENERGY", 8),
    ("PHARMA", 7)
]

# ----------------------------
# News Panel
# ----------------------------

news_frame = tk.LabelFrame(
    content_frame,
    text="News Feed",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b",
    width=350,
    height=180
)

news_frame.grid(
    row=0,
    column=2,
    rowspan=1,
    padx=(6, 0),
    pady=(0, 6),
    sticky="nsew"
)

news_frame.grid_rowconfigure(0, weight=3)
news_frame.grid_rowconfigure(1, weight=2)
news_frame.grid_columnconfigure(0, weight=1)

# ----------------------------
# Chart Panel
# ----------------------------

chart_frame = tk.LabelFrame(
    content_frame,
    text="Price Chart",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b",
    height=360
)

chart_frame.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=(0, 6),
    pady=(0, 6),
    sticky="nsew"
)

# ----------------------------
# Achievements Panel
# ----------------------------

achievement_frame = tk.LabelFrame(
    content_frame,
    text="Achievements",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b",
    height=140
)

# Keep Achievement panel at a fixed height
achievement_frame.configure(height=110)
achievement_frame.grid_propagate(False)

achievement_frame.grid(
    row=2,
    column=0,
    columnspan=3,
    padx=0,
    pady=(0, 0),
    sticky="nsew"
)

# Keep Achievement panel at a fixed height
achievement_frame.grid_propagate(False)
achievement_frame.configure(height=110)

# ----------------------------
# Achievement Grid
# ----------------------------

achievement_grid = tk.Frame(
    achievement_frame,
    bg="#1e293b"
)

achievement_grid.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ----------------------------
# Quick Actions Panel
# ----------------------------

quick_actions_frame = tk.LabelFrame(
    content_frame,
    text="Quick Actions",
    font=("Segoe UI", 14, "bold"),
    fg="white",
    bg="#1e293b"
)

quick_actions_frame.grid(
    row=1,
    column=2,
    padx=(6, 0),
    pady=(0, 6),
    sticky="nsew"
)

quick_actions_frame.grid_propagate(True)

quick_actions_frame.grid_columnconfigure(0, weight=0)
quick_actions_frame.grid_columnconfigure(1, weight=0)

quick_actions_frame.grid_rowconfigure(0, weight=0)
quick_actions_frame.grid_rowconfigure(1, weight=0)

# ----------------------------
# Quick Action Buttons
# ----------------------------

buttons_frame = tk.Frame(
    quick_actions_frame,
    bg="#1e293b"
)

buttons_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

for col in range(2):
    buttons_frame.grid_columnconfigure(
        col,
        weight=1,
        uniform="actions"
    )

for row in range(6):
    buttons_frame.grid_rowconfigure(
        row,
        weight=1,
        uniform="actions"
    )

# ----------------------------
# Row 1
# ----------------------------

buy_stock_button = create_button(
    buttons_frame,
    "📈 Buy Stock",
    "#16a34a"
)

sell_stock_button = create_button(
    buttons_frame,
    "📉 Sell Stock",
    "#dc2626"
)

buy_stock_button.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=4,
    pady=4
)

sell_stock_button.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Row 2
# ----------------------------

next_day_action_button = create_button(
    buttons_frame,
    "⏭ Next Day",
    "#2563eb"
)

next_day_action_button.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Row 3
# ----------------------------

save_action_button = create_button(buttons_frame, "💾 Save", "#2563eb")
load_action_button = create_button(buttons_frame, "📂 Load", "#7c3aed")

save_action_button.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=4,
    pady=4
)

load_action_button.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Row 4
# ----------------------------

portfolio_action_button = create_button(buttons_frame, "📁 Portfolio", "#16a34a")
history_action_button = create_button(buttons_frame, "🕘 History", "#dc2626")

portfolio_action_button.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=4,
    pady=4
)

history_action_button.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Row 5
# ----------------------------

leaderboard_action_button = create_button(buttons_frame, "🏆 Leaderboard", "#0f766e")
statistics_action_button = create_button(buttons_frame, "📊 Statistics", "#475569")

leaderboard_action_button.grid(
    row=4,
    column=0,
    sticky="ew",
    padx=4,
    pady=4
)

statistics_action_button.grid(
    row=4,
    column=1,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Row 6
# ----------------------------

achievement_action_button = create_button(buttons_frame, "🏆 Achievements", "#ca8a04")
help_action_button = create_button(buttons_frame, "❓ Help", "#475569")

achievement_action_button.grid(
    row=5,
    column=0,
    sticky="ew",
    padx=4,
    pady=4
)

help_action_button.grid(
    row=5,
    column=1,
    sticky="ew",
    padx=4,
    pady=4
)

# ----------------------------
# Embedded Chart
# ----------------------------

fig = plt.Figure(
    figsize=(9, 4.6),
    dpi=120,
    facecolor="#1e293b"
)

# Keep fixed margins so the title is never clipped
fig.subplots_adjust(
    left=0.08,
    right=0.98,
    bottom=0.16,
    top=0.82
)

ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(
    fig,
    master=chart_frame
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=6,
    pady=(12, 6)
)

# ----------------------------
# Selected stock used by chart and popups
# ----------------------------

chart_selected_stock = tk.StringVar()

chart_selected_stock.set("TECH")

chart_selected_stock.trace_add(
    "write",
    lambda *args: update_chart()
)

# Keep dashboard panel size
news_frame.grid_propagate(False)

# ----------------------------
# Scrollable News Container
# ----------------------------

news_canvas = tk.Canvas(
    news_frame,
    bg="#162033",
    highlightthickness=0,
    borderwidth=0
)

news_scrollbar = tk.Scrollbar(
    news_frame,
    orient="vertical",
    command=news_canvas.yview,
    width=3,
    relief="flat",
    bd=0,
    bg="#162033",
    activebackground="#1e293b",
    troughcolor="#162033",
    highlightthickness=0
)

news_container = tk.Frame(
    news_canvas,
    bg="#162033"
)

news_container.bind(
    "<Configure>",
    lambda e: news_canvas.configure(
        scrollregion=news_canvas.bbox("all")
    )
)

news_window = news_canvas.create_window(
    (0, 0),
    window=news_container,
    anchor="nw"
)

# Keep the news container the same width as the canvas
def resize_news_container(event):
    news_canvas.itemconfigure(
        news_window,
        width=event.width
    )

news_canvas.bind(
    "<Configure>",
    resize_news_container
)

news_canvas.configure(
    yscrollcommand=news_scrollbar.set
)

news_canvas.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(10, 0),
    pady=(10, 10)
)

news_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns",
    pady=(10, 10),
    padx=(4, 10)
)

# ----------------------------
# Empty News Placeholder
# ----------------------------

empty_news_label = tk.Label(
    news_container,
    text="No latest market news",
    bg="#162033",
    fg="#94a3b8",
    font=("Segoe UI", 11, "italic")
)

empty_news_label.pack(
    expand=True,
    pady=8
)

# ----------------------------
# Create Modern News Card
# ----------------------------

def create_news_card(message):
    """
    Creates a modern news card inside the News Feed.
    UI only.
    """

    card = tk.Frame(
        news_container,
        bg="#1e293b",
        bd=0,
        highlightbackground="#334155",
        highlightthickness=1
    )

    card.pack(
        fill="x",
        padx=4,
        pady=1
    )

    icon = tk.Label(
        card,
        text="📰",
        bg="#1e293b",
        fg="#38bdf8",
        font=("Segoe UI Emoji", 16)
    )

    icon.pack(
        side="left",
        padx=(6, 5),
        pady=4
    )

    text = tk.Label(
        card,
        text=message,
        justify="left",
        anchor="w",
        wraplength=240,
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 10)
    )

    text.pack(
        fill="x",
        expand=True,
        padx=(0, 6),
        pady=4
    )

    news_canvas.update_idletasks()

    news_canvas.configure(
        scrollregion=news_canvas.bbox("all")
    )

    news_canvas.yview_moveto(1)

# ----------------------------
# Add News Entry
# ----------------------------

def add_news(message):
    """
    Adds a news item to the history and displays it
    as a modern news card.
    """

    global empty_news_label

    news_history.append(message)

    # Remove placeholder message when first news arrives
    for widget in news_container.winfo_children():

        if isinstance(widget, tk.Label):
            widget.destroy()

    # Remove placeholder when first news arrives
    if 'empty_news_label' in globals() and empty_news_label.winfo_exists():
        empty_news_label.destroy()

    create_news_card(message)


# ----------------------------
# Refresh Portfolio Table
# ----------------------------

def refresh_portfolio_table():

    for stock in portfolio:

        shares = portfolio[stock]

        value = shares * stocks[stock]

        profit = (
            stocks[stock]
            - average_buy_price[stock]
        ) * shares

        if shares == 0:
            profit = 0

        if profit > 0:
            pl_text = f"+₹{profit:,.0f}"

        elif profit < 0:
            pl_text = f"-₹{abs(profit):,.0f}"

        else:
            pl_text = "₹0"

        # Set row color based on profit/loss
        if profit > 0:
            row_tag = "profit"

        elif profit < 0:
            row_tag = "loss"

        else:
            row_tag = "neutral"

        portfolio_tree.item(
            stock,
            values=(
                stock,
                shares,
                f"₹{average_buy_price[stock]:,.0f}",
                f"₹{stocks[stock]:,.0f}",
                f"₹{value:,.0f}",
                pl_text
            ),
            tags=(row_tag,)
        )

# ----------------------------
# Update Dashboard Chart
# ----------------------------

def update_chart():

    selected = chart_selected_stock.get()

    ax.clear()

    fig.patch.set_facecolor("#1e293b")
    ax.set_facecolor("#1e293b")

    prices = price_history[selected]

    ax.plot(
        range(len(prices)),
        prices,
        color="#38bdf8",
        linewidth=2.5
    )

    # ---------- Stable Y Axis ----------
    min_price = min(prices)
    max_price = max(prices)

    if min_price == max_price:
        padding = max(20, min_price * 0.20)
    else:
        padding = max(20, (max_price - min_price) * 0.20)

    ax.set_ylim(
        min_price - padding,
        max_price + padding
    )

    # ---------- Stable X Axis ----------
    ax.set_xlim(
        0,
        max(7, len(prices) - 1)
    )

    ax.tick_params(
        colors="white",
        labelsize=10
    )

    ax.grid(
        True,
        color="#475569",
        alpha=0.35
    )

    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")

    # DO NOT call fig.tight_layout() here.
    # It causes the chart to resize every redraw.

    canvas.draw_idle()

# ----------------------------
# Status Bar
# ----------------------------

status_bar = tk.Label(
    root,
    text="Welcome to Stock Market Survival",
    bg="#111827",
    fg="#facc15",
    font=("Arial", 10, "bold"),
    anchor="w",
    padx=15
)

status_bar.pack(
    side="bottom",
    fill="x"
)

# ----------------------------
# Update Status Bar
# ----------------------------

def update_status(message):

    status_bar.config(
        text=message
    )

# ----------------------------
# Game Notification
# ----------------------------

def show_notification(message):

    popup = tk.Toplevel(root)

    popup.overrideredirect(True)

    popup.configure(bg="#111827")

    popup.geometry(
       f"320x70+{root.winfo_screenwidth()-350}+120"
    )

    tk.Label(
        popup,
        text=message,
        bg="#111827",
        fg="white",
        font=("Arial", 10, "bold"),
        wraplength=280
    ).pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )

    popup.after(
        3000,
        popup.destroy
    )

# ----------------------------
# Buy Stock Popup
# ----------------------------

def open_buy_popup():

    popup = tk.Toplevel(root)
    popup.title("Buy Stock")
    popup.configure(bg="#1e293b")
    popup.resizable(False, False)
    popup.transient(root)
    
    popup.grab_set()

    center_popup(
        popup,
        root,
        340,
        190
    )

    tk.Label(
        popup,
        text="Stock",
        bg=POPUP_BG,
        fg="white",
        font=("Segoe UI",10,"bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    popup_stock = ttk.Combobox(
        popup,
        values=list(stocks.keys()),
        state="readonly",
        width=18
    )
    popup_stock.set(chart_selected_stock.get())

    popup_stock.pack(
        padx=15,
        fill="x"
    )

    tk.Label(
        popup,
        text="Quantity",
        bg=POPUP_BG,
        fg="white",
        font=ENTRY_FONT
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 8)
    )

    popup_quantity = tk.Entry(
        popup,
        font=("Segoe UI", 10)
    )

    popup_quantity.pack(
        padx=15,
        fill="x"
    )
    
    popup_quantity.focus_set()

    popup.bind("<Return>", lambda e: confirm_buy())
    popup.bind("<Escape>", lambda e: popup.destroy())

    button_frame = tk.Frame(
        popup,
        bg="#1e293b"
    )

    button_frame.pack(
        fill="x",
        padx=15,
        pady=15
    )

    def confirm_buy():

        chart_selected_stock.set(popup_stock.get())

        buy_stock_from_popup(
            popup_stock.get(),
            popup_quantity.get()
        )

        popup.destroy()

    create_popup_button(
        button_frame,
        "Buy",
        "#16a34a",
        confirm_buy
    ).pack(side="left")

    create_popup_button(
        button_frame,
        "Cancel",
        "#475569",
        popup.destroy
    ).pack(side="right")

# ----------------------------
# Sell Stock Popup
# ----------------------------

def open_sell_popup():

    popup = tk.Toplevel(root)
    popup.title("Sell Stock")
    popup.configure(bg="#1e293b")
    popup.resizable(False, False)
    popup.transient(root)
    
    popup.grab_set()

    popup.update_idletasks()

    width = 340
    height = 190

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)

    popup.geometry(f"{width}x{height}+{x}+{y}")

    tk.Label(
        popup,
        text="Stock",
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=15, pady=(15, 5))

    popup_stock = ttk.Combobox(
        popup,
        values=list(stocks.keys()),
        state="readonly",
        width=18
    )

    popup_stock.set(chart_selected_stock.get())
    popup_stock.pack(padx=15, fill="x")

    tk.Label(
        popup,
        text="Quantity",
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 5))

    popup_quantity = tk.Entry(
        popup,
        font=("Segoe UI", 10)
    )

    popup_quantity.pack(
        padx=15,
        fill="x"
    )

    popup_quantity.focus_set()

    button_frame = tk.Frame(
        popup,
        bg="#1e293b"
    )

    button_frame.pack(
        fill="x",
        padx=15,
        pady=15
    )

    def confirm_sell():

        chart_selected_stock.set(popup_stock.get())

        sell_stock_from_popup(
            popup_stock.get(),
            popup_quantity.get()
        )

        popup.destroy()

    tk.Button(
        button_frame,
        text="Sell",
        command=confirm_sell,
        bg="#dc2626",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=12
    ).pack(side="left")

    tk.Button(
        button_frame,
        text="Cancel",
        command=popup.destroy,
        bg="#475569",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=12
    ).pack(side="right")

def buy_stock_from_popup(stock, quantity_text):
    global cash
    global buy_trades

    try:
        quantity = int(quantity_text)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return

    if quantity <= 0:
        messagebox.showerror("Error", "Quantity must be greater than 0.")
        return

    cost = stocks[stock] * quantity

    if cost > cash:
        messagebox.showwarning("Insufficient Funds", "Not enough cash available.")
        return

    cash -= cost

    old_shares = portfolio[stock]

    if old_shares == 0:
        average_buy_price[stock] = stocks[stock]
    else:
        total_cost = (
            average_buy_price[stock] * old_shares
        ) + (stocks[stock] * quantity)

        average_buy_price[stock] = total_cost / (old_shares + quantity)

    portfolio[stock] += quantity

    transaction_history.append(
        f"BUY | Day {day} | {stock} | {quantity} shares | ₹{stocks[stock]}"
    )

    buy_trades += 1

    cash_label.config(text=f"₹{cash:,}")
    net_worth_label.config(text=f"₹{calculate_net_worth():,}")
    portfolio_value_label.config(text=f"₹{calculate_portfolio_value():,}")

    update_best_net_worth()
    update_profit_loss_display()
    refresh_portfolio_table()

    update_status(f"Bought {quantity} shares of {stock}")
    show_notification(f"Bought {quantity} {stock} shares")

    check_achievements()

def sell_stock_from_popup(stock, quantity_text):
    global cash
    global sell_trades

    try:
        quantity = int(quantity_text)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return

    if quantity <= 0:
        messagebox.showerror("Error", "Quantity must be greater than 0.")
        return

    if portfolio[stock] < quantity:
        messagebox.showwarning("Warning", "Not enough shares.")
        return

    cash += stocks[stock] * quantity
    portfolio[stock] -= quantity

    transaction_history.append(
        f"SELL | Day {day} | {stock} | {quantity} shares | ₹{stocks[stock]}"
    )

    sell_trades += 1

    cash_label.config(text=f"₹{cash:,}")
    net_worth_label.config(text=f"₹{calculate_net_worth():,}")
    portfolio_value_label.config(text=f"₹{calculate_portfolio_value():,}")

    update_best_net_worth()
    update_profit_loss_display()
    refresh_portfolio_table()

    update_status(f"Sold {quantity} shares of {stock}")
    show_notification(f"Sold {quantity} {stock} shares")

    check_achievements()

# ----------------------------
# Advance Market One Day
# ----------------------------

def next_day():

    global day
    global previous_prices

    # Save yesterday's prices
    previous_prices = stocks.copy()

    day += 1

    # Update day label
    day_label.config(
        text=f"Day {day} / 30"
    )

    # Random market movement
    for stock in stocks:

        # Difficulty-based volatility
        if difficulty == "Easy":

            change = random.choice(
                [-10, -5, 5, 10]
            )

        elif difficulty == "Hard":

            change = random.choice(
                [-30, -25, -20, 20, 25, 30]
            )

        else:

            change = random.choice(
                [-20, -15, -10, 10, 15, 20]
            )

        stocks[stock] += change

        if stocks[stock] < 10:
            stocks[stock] = 10

        # Store daily price for chart history
        price_history[stock].append(
            stocks[stock]
        )

    # ----------------------------
    # Market Event System
    # ----------------------------

    special_event_happened = (random.randint(1, 10) == 1)

    if special_event_happened:

        event = random.choice(special_events)

        title = event[0]
        affected_stock = event[1]
        effect = event[2]

        add_news(
            f"SPECIAL EVENT: {title}"
        )

    else:

        news = random.choice(news_events)

        title = news[0]
        affected_stock = news[1]
        effect = news[2]
        description = news[3]

        add_news(
            f"{title} | {description}"
        )

    # Apply effect
    if affected_stock == "ALL":

        for stock in stocks:

            stocks[stock] += effect

            if stocks[stock] < 10:
                stocks[stock] = 10

    else:

        stocks[affected_stock] += effect

        if stocks[affected_stock] < 10:
            stocks[affected_stock] = 10

    # Update portfolio value display
    portfolio_value_label.config(
        text=f"₹{calculate_portfolio_value():,}"
    )

    update_profit_loss_display()

    # Refresh Market Overview Table
    for stock in stocks:

        current_price = stocks[stock]
        old_price = previous_prices[stock]

        change = current_price - old_price

        if old_price > 0:

            percent_change = (
                change / old_price
            ) * 100

        else:

            percent_change = 0

        if change > 0:
            arrow = "▲"

        elif change < 0:
            arrow = "▼"

        else:
            arrow = "■"

        if change > 0:

            market_tree.item(
                stock,
                tags=("gain",)
            )

        elif change < 0:

            market_tree.item(
                stock,
                tags=("loss",)
            )

        else:

            market_tree.item(
                stock,
                tags=("neutral",)
            )

        # Format movement text
        if change > 0:
            movement_text = (
                f"+₹{abs(change)} "
                f"(+{abs(percent_change):.2f}%) ▲"
            )

        elif change < 0:
            movement_text = (
                f"-₹{abs(change)} "
                f"(-{abs(percent_change):.2f}%) ▼"
            )

        else:
            movement_text = "₹0 (0.00%) →"

        market_tree.item(
            stock,
            values=(
                stock,
                f"₹{current_price}",
                movement_text
            )
        )

    # Market trend indicator will be reintroduced later.
    # (Temporarily disabled to prevent runtime error.)

    update_chart()

    net_worth_label.config(
        text=f"₹{calculate_net_worth():,}"
    )

    update_best_net_worth()

    # ----------------------------
    # Random Dividend Chance
    # 15% probability
    # ----------------------------

    if random.randint(1, 100) <= 15:

        pay_dividend()

    # ----------------------------
    # Random Stock Split Chance
    # 5% probability
    # ----------------------------

    if random.randint(1, 100) <= 5:

        stock_split()

    # Check achievements
    check_achievements()

    update_status(
        f"Day {day} completed | Net Worth ₹{calculate_net_worth():,}"
    )

    # Check game status
    check_game_status()

# ----------------------------
# Calculate Net Worth
# ----------------------------

def calculate_net_worth():

    total = cash

    for stock in portfolio:
        total += portfolio[stock] * stocks[stock]

    return total

# ----------------------------
# Track Best Net Worth
# ----------------------------

def update_best_net_worth():

    global best_net_worth

    current = calculate_net_worth()

    if current > best_net_worth:
        best_net_worth = current

# ----------------------------
# Calculate Portfolio Value
# ----------------------------

def calculate_portfolio_value():

    total = 0

    for stock in portfolio:
        total += portfolio[stock] * stocks[stock]

    return total

# ----------------------------
# Calculate Profit Loss
# ----------------------------

def calculate_total_profit_loss():

    total_pl = 0

    for stock in portfolio:

        shares = portfolio[stock]

        if shares > 0:

            total_pl += (
                (stocks[stock] -
                 average_buy_price[stock])
                * shares
            )

    return total_pl

# ----------------------------
# Dividend Payout System
# ----------------------------

def pay_dividend():

    global cash

    stock, dividend = random.choice(
        dividend_events
    )

    shares = portfolio[stock]

    if shares <= 0:
        return

    payout = shares * dividend

    cash += payout

    # Update news panel
    add_news(
        f"Dividend: {stock} paid ₹{payout:,}"
    )

    show_notification(
        f"Dividend received ₹{payout:,}"
    )

    # Refresh cash display
    cash_label.config(
        text=f"₹{cash:,}"
    )

    net_worth_label.config(
        text=f"₹{calculate_net_worth():,}"
    )

    portfolio_value_label.config(
        text=f"₹{calculate_portfolio_value():,}"
    )

    update_best_net_worth()

    update_profit_loss_display()

# ----------------------------
# Stock Split System
# ----------------------------

def stock_split():

    stock = random.choice(
        list(stocks.keys())
    )

    # Prevent repeated splits
    if day - last_split_day[stock] < 10:
        return

    # Split only if price is high
    if stocks[stock] < 250:
        return

    old_price = stocks[stock]

    stocks[stock] = round(
        stocks[stock] / 2
    )

    portfolio[stock] *= 2

    if average_buy_price[stock] > 0:
        average_buy_price[stock] /= 2

    last_split_day[stock] = day

    # Update portfolio display
    refresh_portfolio_table()

    add_news(
        f"Stock Split: {stock} executed 2-for-1 split"
    )

    show_notification(
        f"{stock} completed a stock split"
    )

# ----------------------------
# Calculate Total Profit Loss
# ----------------------------

def update_profit_loss_display():

    profit = calculate_total_profit_loss()

    color = "#22c55e"

    if profit < 0:
        color = "#ef4444"

    profit_loss_label.config(
        text=f"₹{profit:,.0f}",
        fg=color
    )

# ----------------------------
# Check Win/Lose Conditions
# ----------------------------

# ----------------------------
# Handles:
# 1. Bankruptcy
# 2. Victory
# 3. End of Game
# ----------------------------

def check_game_status():

    global game_over

    if game_over:
        return

    net_worth = calculate_net_worth()

    # ----------------------------
    # Bankruptcy Condition
    # ----------------------------

    if net_worth <= 10000:

        game_over = True

        messagebox.showerror(
            "Bankrupt!",
            f"""
    You went bankrupt.

    Final Net Worth:
    ₹{net_worth:,}

    Day Reached:
    {day}

    Better luck next time.
    """
        )

        save_score_to_leaderboard()

        root.destroy()

        return

    if net_worth >= 1000000:

        game_over = True

        messagebox.showinfo(
            "🏆 Market Legend",
            f"""
    Congratulations!

    Final Net Worth:
    ₹{net_worth:,}

    Best Net Worth:
    ₹{best_net_worth:,}

    Buy Trades:
    {buy_trades}

    Sell Trades:
    {sell_trades}

    Achievements Unlocked:
    {len(achievements_unlocked)}

    You became a Market Legend!
    """
        )
    
        save_score_to_leaderboard()
        root.destroy()

    elif day >= 30:

        game_over = True

        portfolio_summary = ""

        for stock in portfolio:
            portfolio_summary += (
                f"{stock}: {portfolio[stock]} shares\n"
            )

        messagebox.showinfo(
            "Game Summary",
            f"""
Day Reached: {day}

Final Net Worth:
₹{net_worth:,}

Best Net Worth:
₹{best_net_worth:,}

Cash:
₹{cash:,}

Buy Trades:
{buy_trades}

Sell Trades:
{sell_trades}

Portfolio:

{portfolio_summary}

Achievements:
{len(achievements_unlocked)}
"""
        )

        save_score_to_leaderboard()
        root.destroy()

# ----------------------------
# Achievement System
# ----------------------------

def check_achievements():

    net_worth = calculate_net_worth()

    # First Trade Achievement
    if (
        "First Trade" not in achievements_unlocked
        and sum(portfolio.values()) > 0
    ):
        achievements_unlocked.add("First Trade")

        # Refresh achievement panel
        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "First Trade\n\nBought your first stock."
        )

    # Investor Achievement
    if (
        "Investor" not in achievements_unlocked
        and net_worth >= 200000
    ):
        achievements_unlocked.add("Investor")
        
        # Refresh achievement panel
        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Investor\n\nReached ₹200,000 net worth."
        )

    # Market Tycoon Achievement
    if (
        "Market Tycoon" not in achievements_unlocked
        and net_worth >= 500000
    ):
        achievements_unlocked.add("Market Tycoon")

        # Refresh achievement panel
        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Market Tycoon\n\nReached ₹500,000 net worth."
        )
    
    # Trader Achievement
    if (
        "Trader" not in achievements_unlocked
        and (buy_trades + sell_trades) >= 10
    ):
        achievements_unlocked.add("Trader")

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Trader\n\nCompleted 10 trades."
        )

    # Active Trader Achievement
    if (
        "Active Trader" not in achievements_unlocked
        and (buy_trades + sell_trades) >= 25
    ):
        achievements_unlocked.add("Active Trader")

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Active Trader\n\nCompleted 25 trades."
        )

    # Millionaire Achievement
    if (
        "Millionaire" not in achievements_unlocked
        and net_worth >= 1000000
    ):
        achievements_unlocked.add("Millionaire")

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Millionaire\n\nReached ₹1,000,000 net worth."
        )

    # Diamond Hands Achievement
    if (
        "Diamond Hands" not in achievements_unlocked
        and day >= 20
    ):
        achievements_unlocked.add("Diamond Hands")

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Diamond Hands\n\nSurvived until Day 20."
        )

    # Diversified Investor Achievement
    if (
        "Diversified Investor" not in achievements_unlocked
        and all(shares > 0 for shares in portfolio.values())
    ):
        achievements_unlocked.add("Diversified Investor")

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Diversified Investor\n\nOwn all 6 stocks."
        )

    if (
        "Survivor"
        not in achievements_unlocked
        and day >= 30
    ):

        achievements_unlocked.add(
            "Survivor"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Survivor\n\nReached Day 30."
        )

    # ----------------------------
    # Profit Maker
    # ----------------------------

    if (
        "Profit Maker" not in achievements_unlocked
        and calculate_total_profit_loss() >= 50000
    ):

        achievements_unlocked.add(
            "Profit Maker"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Profit Maker\n\nEarned ₹50,000 profit."
        )

    # ----------------------------
    # Wealth Builder
    # ----------------------------

    if (
        "Wealth Builder" not in achievements_unlocked
        and best_net_worth >= 300000
    ):

        achievements_unlocked.add(
            "Wealth Builder"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Wealth Builder\n\nReached ₹300,000 net worth."
        )

    # ----------------------------
    # Dividend Collector
    # ----------------------------

    if (
        "Dividend Collector"
        not in achievements_unlocked
        and cash >= 250000
    ):

        achievements_unlocked.add(
            "Dividend Collector"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Dividend Collector\n\nBuilt large cash reserves."
        )

    # ----------------------------
    # Stock Master
    # ----------------------------

    if (
        "Stock Master"
        not in achievements_unlocked
        and any(
            shares >= 1000
            for shares in portfolio.values()
        )
    ):

        achievements_unlocked.add(
            "Stock Master"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Stock Master\n\nOwned 1000 shares of one stock."
        )

    # ----------------------------
    # Survivor Elite
    # ----------------------------

    if (
        "Survivor Elite"
        not in achievements_unlocked
        and day >= 25
    ):

        achievements_unlocked.add(
            "Survivor Elite"
        )

        update_achievement_display()

        messagebox.showinfo(
            "🏆 Achievement Unlocked",
            "Survivor Elite\n\nReached Day 25."
        )


# ----------------------------
# Refresh Achievement Display
# ----------------------------

def update_achievement_display():
    """Refresh compact dashboard achievement panel."""

    # Clear previous dashboard cards
    for widget in achievement_grid.winfo_children():
        widget.destroy()

    achievement_names = [
        ("First Trade", "First"),
        ("Investor", "Investor"),
        ("Trader", "Trader"),
        ("Active Trader", "Active"),
        ("Market Tycoon", "Tycoon"),
        ("Millionaire", "Million"),
        ("Diamond Hands", "Diamond"),
        ("Diversified Investor", "Diversify"),
        ("Survivor", "Survivor"),
        ("Profit Maker", "Profit"),
        ("Wealth Builder", "Wealth"),
        ("Dividend Collector", "Dividend"),
        ("Stock Master", "Master"),
        ("Survivor Elite", "Elite")
    ]

    # Always recreate the dashboard cards
    for widget in achievement_grid.winfo_children():
        widget.destroy()

    for index, (achievement, display_name) in enumerate(achievement_names):

        unlocked = achievement in achievements_unlocked

        card = tk.Frame(
            achievement_grid,
            width=94,
            height=94,
            bg="#182437",
            highlightbackground="#22c55e" if unlocked else "#334155",
            highlightthickness=1
        )

        # Prevent the frame from resizing to fit its contents
        card.grid_propagate(False)
        card.pack_propagate(False)

        card.grid_propagate(False)

        # Icon
        tk.Label(
            card,
            text="🏆" if unlocked else "🔒",
            font=("Segoe UI Emoji", 18),
            fg="#22c55e" if unlocked else "#94a3b8",
            bg="#182437"
        ).pack(pady=(10, 4))

        # Achievement name (always reserve space for TWO lines)
        name = tk.Label(
            card,
            text=achievement,
            wraplength=72,
            justify="center",
            height=2,              # <-- Always reserve two text lines
            anchor="n",            # <-- Text starts at the top of the reserved area
            font=("Segoe UI", 8, "bold"),
            fg="#f8fafc" if unlocked else "#94a3b8",
            bg="#182437"
        )

        name.pack(
            fill="x",
            padx=4,
            pady=(0, 4)
        )

        # Keep every card perfectly square
        card.grid(
            row=0,
            column=index,
            padx=6,
            pady=6,
            ipadx=0,
            ipady=0
        )

        # Display the card in a single horizontal row
        card.grid(
            row=0,
            column=index,
            padx=6,
            pady=6
        )

    # Keep all cards in one horizontal row
    for column in range(len(achievement_names)):
        achievement_grid.grid_columnconfigure(
            column,
            weight=0
        )

# ----------------------------
# View Achievements
# ----------------------------

def view_achievements():

    achievement_window = tk.Toplevel(root)

    achievement_window.title("Achievements")
    achievement_window.configure(bg="#0f172a")
    achievement_window.resizable(False, False)
    achievement_window.transient(root)
    achievement_window.grab_set()

    center_popup(
        achievement_window,
        root,
        760,
        540
    )

    tk.Label(
        achievement_window,
        text="🏆 ACHIEVEMENTS",
        font=("Segoe UI", 22, "bold"),
        fg="#facc15",
        bg="#0f172a"
    ).pack(
        pady=(18, 12)
    )

    table_frame = tk.Frame(
        achievement_window,
        bg="#1e293b"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    achievement_list = tk.Listbox(
        table_frame,
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 11),
        borderwidth=0,
        highlightthickness=0,
        selectbackground="#2563eb",
        selectforeground="white",
        activestyle="none"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=achievement_list.yview
    )

    achievement_list.configure(
        yscrollcommand=scrollbar.set
    )

    achievement_list.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    achievement_names = [
        "First Trade",
        "Investor",
        "Trader",
        "Active Trader",
        "Market Tycoon",
        "Millionaire",
        "Diamond Hands",
        "Diversified Investor",
        "Survivor",
        "Profit Maker",
        "Wealth Builder",
        "Dividend Collector",
        "Stock Master",
        "Survivor Elite"
    ]

    for achievement in achievement_names:

        if achievement in achievements_unlocked:
            achievement_list.insert(
                tk.END,
                f"🟢  {achievement}"
            )
        else:
            achievement_list.insert(
                tk.END,
                f"⚪  {achievement} (Locked)"
            )

    footer = tk.Frame(
        achievement_window,
        bg="#0f172a"
    )

    footer.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Label(
        footer,
        text=f"Unlocked : {len(achievements_unlocked)} / {len(achievement_names)}",
        bg="#0f172a",
        fg="#facc15",
        font=("Segoe UI", 11, "bold")
    ).pack(
        side="left"
    )

    tk.Button(
        footer,
        text="Close",
        command=achievement_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18
    ).pack(
        side="right"
    )

# ----------------------------
# Save Game
# ----------------------------

def save_game():

    data = {

        # Player name
        "player_name": player_name,

        # Difficulty level
        "difficulty": difficulty,

        # Historical prices
        "price_history": price_history,

        # Statistics
        "buy_trades": buy_trades,
        "sell_trades": sell_trades,
        "best_net_worth": best_net_worth,

        # Current game state
        "cash": cash,
        "day": day,

        # Stock prices
        "stocks": stocks,

        # Portfolio holdings
        "portfolio": portfolio,

        # Save average purchase prices
        "average_buy_price": average_buy_price,

        "last_split_day": last_split_day,

        # Transaction history
        "transaction_history": transaction_history,

        # Achievements
        "achievements": list(
            achievements_unlocked
        )
    }

    with open(
        "savegame.json",
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    messagebox.showinfo(
        "Game Saved",
        "Progress saved successfully."
    )

# ----------------------------
# Load Game
# ----------------------------

def load_game():

    global cash
    global day
    global player_name
    global price_history
    global buy_trades
    global sell_trades
    global best_net_worth
    global average_buy_price
    global last_split_day
    global transaction_history

    try:

        with open(
            "savegame.json",
            "r"
        ) as file:

            data = json.load(file)

        player_name = data.get(
            "player_name",
            "Player"
        )

        global difficulty

        difficulty = data.get(
            "difficulty",
            "Normal"
        )

        difficulty_label.config(
            text=difficulty
        )

        price_history = data.get(
            "price_history",
            price_history
        )

        buy_trades = data.get(
            "buy_trades",
            0
        )

        sell_trades = data.get(
            "sell_trades",
            0
        )

        best_net_worth = data.get(
            "best_net_worth",
            100000
        )

    except FileNotFoundError:

        messagebox.showwarning(
            "Load Failed",
            "No save file found."
        )

        return

    # Restore values
    cash = data["cash"]
    day = data["day"]

    stocks.update(
        data["stocks"]
    )

    portfolio.update(
        data["portfolio"]
    )

    average_buy_price.update(
        data.get(
            "average_buy_price",
            average_buy_price
        )
    )

    # Restore average buy prices
    last_split_day.update(
        data.get(
            "last_split_day",
            last_split_day
        )
    )

    transaction_history.clear()

    transaction_history.extend(
        data.get(
            "transaction_history",
            []
        )
    )

    achievements_unlocked.clear()

    achievements_unlocked.update(
        data["achievements"]
    )

    # Refresh displays
    cash_label.config(
        text=f"₹{cash:,}"
    )

    day_label.config(
        text=f"Day {day} / 30"
    )

    net_worth_label.config(
        text=f"₹{calculate_net_worth():,}"
    )

    portfolio_value_label.config(
        text=f"₹{calculate_portfolio_value():,}"
    )

    # Refresh profit/loss label
    update_profit_loss_display()

    # Refresh Market Overview Table
    for stock in stocks:

        market_tree.item(
            stock,
            values=(
                stock,
                f"₹{stocks[stock]}",
                "₹0 (0.00%) →"
            )
        )

    # Refresh portfolio labels
    refresh_portfolio_table()

    # Refresh achievement panel
    update_achievement_display() 

    messagebox.showinfo(
        "Game Loaded",
        "Save loaded successfully."
    )

# ----------------------------
# Save Score To Leaderboard
# ----------------------------

def save_score_to_leaderboard():

    score = calculate_net_worth()

    leaderboard_file = "leaderboard.json"

    # Create file if missing
    if not os.path.exists(
        leaderboard_file
    ):

        with open(
            leaderboard_file,
            "w"
        ) as file:

            json.dump(
                [],
                file
            )

    # Load existing scores
    with open(
        leaderboard_file,
        "r"
    ) as file:

        scores = json.load(file)

    # Add current score
    scores.append({
        "name": player_name,
        "score": score
    })

    # Highest first
    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Keep Top 10
    scores = scores[:10]

    # Save back
    with open(
        leaderboard_file,
        "w"
    ) as file:

        json.dump(
            scores,
            file,
            indent=4
        )

# ----------------------------
# View Leaderboard
# ----------------------------

def view_leaderboard():

    leaderboard_file = "leaderboard.json"

    if not os.path.exists(leaderboard_file):

        messagebox.showinfo(
            "Leaderboard",
            "No scores yet."
        )

        return

    with open(
        leaderboard_file,
        "r"
    ) as file:

        scores = json.load(file)

    leaderboard_window = tk.Toplevel(root)

    leaderboard_window.title("Leaderboard")
    leaderboard_window.configure(bg="#0f172a")
    leaderboard_window.resizable(False, False)
    leaderboard_window.transient(root)
    leaderboard_window.grab_set()

    center_popup(
        leaderboard_window,
        root,
        760,
        540
    )

    tk.Label(
        leaderboard_window,
        text="TOP PLAYERS",
        font=("Segoe UI", 22, "bold"),
        fg="#facc15",
        bg="#0f172a"
    ).pack(
        pady=(18, 12)
    )

    table_frame = tk.Frame(
        leaderboard_window,
        bg="#1e293b"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    leaderboard_tree = ttk.Treeview(
        table_frame,
        columns=(
            "Rank",
            "Player",
            "Score"
        ),
        show="headings",
        height=10
    )

    leaderboard_tree.heading(
        "Rank",
        text="Rank"
    )

    leaderboard_tree.heading(
        "Player",
        text="Player"
    )

    leaderboard_tree.heading(
        "Score",
        text="Net Worth"
    )

    leaderboard_tree.column(
        "Rank",
        width=80,
        anchor="center"
    )

    leaderboard_tree.column(
        "Player",
        width=280,
        anchor="center"
    )

    leaderboard_tree.column(
        "Score",
        width=260,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=leaderboard_tree.yview
    )

    leaderboard_tree.configure(
        yscrollcommand=scrollbar.set
    )

    leaderboard_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for rank, entry in enumerate(
        scores,
        start=1
    ):

        leaderboard_tree.insert(
            "",
            "end",
            values=(
                rank,
                entry["name"],
                f"₹{entry['score']:,}"
            )
        )

    footer = tk.Frame(
        leaderboard_window,
        bg="#0f172a"
    )

    footer.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Button(
        footer,
        text="Close",
        command=leaderboard_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18
    ).pack(
        side="right"
    )

# ----------------------------
# View Statistics
# ----------------------------

def view_statistics():

    stats_window = tk.Toplevel(root)
    stats_window.title("Statistics")
    stats_window.configure(bg="#0f172a")
    stats_window.resizable(False, False)
    stats_window.transient(root)
    stats_window.grab_set()

    center_popup(stats_window, root, 700, 560)

    tk.Label(
        stats_window,
        text="PLAYER STATISTICS",
        font=("Segoe UI", 22, "bold"),
        fg="#38bdf8",
        bg="#0f172a"
    ).pack(pady=(18, 12))

    container = tk.Frame(
        stats_window,
        bg="#1e293b"
    )

    container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    stats = [
        ("Player", player_name),
        ("Difficulty", difficulty),
        ("Current Day", day),
        ("Cash", f"₹{cash:,}"),
        ("Net Worth", f"₹{calculate_net_worth():,}"),
        ("Best Net Worth", f"₹{best_net_worth:,}"),
        ("Portfolio Value", f"₹{calculate_portfolio_value():,}"),
        ("Profit / Loss", f"₹{calculate_total_profit_loss():,.0f}"),
        ("Buy Trades", buy_trades),
        ("Sell Trades", sell_trades),
        ("Achievements", len(achievements_unlocked))
    ]

    for row, (title, value) in enumerate(stats):

        tk.Label(
            container,
            text=title,
            bg="#1e293b",
            fg="#94a3b8",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(25, 40),
            pady=8
        )

        tk.Label(
            container,
            text=value,
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 11),
            anchor="w"
        ).grid(
            row=row,
            column=1,
            sticky="w",
            pady=8
        )

    tk.Button(
        stats_window,
        text="Close",
        command=stats_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=20
    ).pack(pady=(0, 15))

# ----------------------------
# Portfolio Summary
# ----------------------------

def view_portfolio_summary():

    summary_window = tk.Toplevel(root)

    summary_window.title("Portfolio Summary")
    summary_window.configure(bg="#0f172a")
    summary_window.resizable(False, False)
    summary_window.transient(root)
    summary_window.grab_set()

    center_popup(summary_window, root, 760, 500)

    tk.Label(
        summary_window,
        text="PORTFOLIO SUMMARY",
        font=("Segoe UI", 22, "bold"),
        fg="#22c55e",
        bg="#0f172a"
    ).pack(pady=(18, 12))

    table_frame = tk.Frame(
        summary_window,
        bg="#1e293b"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    summary_tree = ttk.Treeview(
        table_frame,
        columns=(
            "Stock",
            "Shares",
            "Price",
            "Value"
        ),
        show="headings",
        height=8
    )

    summary_tree.heading(
        "Stock",
        text="Stock"
    )

    summary_tree.heading(
        "Shares",
        text="Shares"
    )

    summary_tree.heading(
        "Price",
        text="Price"
    )

    summary_tree.heading(
        "Value",
        text="Value"
    )

    summary_tree.column(
        "Stock",
        width=160,
        anchor="center"
    )

    summary_tree.column(
        "Shares",
        width=120,
        anchor="center"
    )

    summary_tree.column(
        "Price",
        width=150,
        anchor="center"
    )

    summary_tree.column(
        "Value",
        width=180,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=summary_tree.yview
    )

    summary_tree.configure(
        yscrollcommand=scrollbar.set
    )

    summary_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    total_value = 0

    for stock in portfolio:

        shares = portfolio[stock]
        price = stocks[stock]
        value = shares * price

        total_value += value

        summary_tree.insert(
            "",
            "end",
            values=(
                stock,
                shares,
                f"₹{price:,}",
                f"₹{value:,}"
            )
        )

    footer = tk.Frame(
        summary_window,
        bg="#0f172a"
    )

    footer.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Label(
        footer,
        text=f"Total Portfolio Value : ₹{total_value:,}",
        font=("Segoe UI", 13, "bold"),
        fg="#facc15",
        bg="#0f172a"
    ).pack(side="left")

    tk.Button(
        footer,
        text="Close",
        command=summary_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18
    ).pack(side="right")

# ----------------------------
# Transaction History
# ----------------------------

def view_transaction_history():

    history_window = tk.Toplevel(root)

    history_window.title("Transaction History")
    history_window.configure(bg="#0f172a")
    history_window.resizable(False, False)
    history_window.transient(root)
    history_window.grab_set()

    center_popup(
        history_window,
        root,
        760,
        560
    )

    tk.Label(
        history_window,
        text="🕘 TRANSACTION HISTORY",
        font=("Segoe UI", 22, "bold"),
        fg="#ef4444",
        bg="#0f172a"
    ).pack(
        pady=(18, 12)
    )

    content_frame = tk.Frame(
        history_window,
        bg="#1e293b"
    )

    content_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    scrollbar = ttk.Scrollbar(content_frame)

    history_text = tk.Text(
        content_frame,
        bg="#1e293b",
        fg="white",
        font=("Consolas", 11),
        wrap="word",
        relief="flat",
        padx=15,
        pady=15,
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(command=history_text.yview)

    history_text.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    if transaction_history:

        for transaction in reversed(transaction_history):

            history_text.insert(
                tk.END,
                f"• {transaction}\n\n"
            )

    else:

        history_text.insert(
            tk.END,
            "No transactions available."
        )

    history_text.config(state="disabled")

    footer = tk.Frame(
        history_window,
        bg="#0f172a"
    )

    footer.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Label(
        footer,
        text=f"Transactions : {len(transaction_history)}",
        bg="#0f172a",
        fg="#facc15",
        font=("Segoe UI", 11, "bold")
    ).pack(
        side="left"
    )

    tk.Button(
        footer,
        text="Close",
        command=history_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18
    ).pack(
        side="right"
    )

# ----------------------------
# Export Report
# ----------------------------

def export_report():

    report = (
        "=====================================\n"
        " STOCK MARKET SURVIVAL REPORT\n"
        "=====================================\n\n"

        f"Player Name : {player_name}\n"
        f"Difficulty  : {difficulty}\n"
        f"Current Day : {day}\n\n"

        "---------- FINANCIALS ----------\n\n"

        f"Cash                 : ₹{cash:,}\n"
        f"Net Worth            : ₹{calculate_net_worth():,}\n"
        f"Best Net Worth       : ₹{best_net_worth:,}\n"
        f"Portfolio Value      : ₹{calculate_portfolio_value():,}\n"
        f"Profit / Loss        : ₹{calculate_total_profit_loss():,.0f}\n\n"

        "---------- TRADING ----------\n\n"

        f"Buy Trades           : {buy_trades}\n"
        f"Sell Trades          : {sell_trades}\n\n"
    )                   

    report += (
        "---------- PORTFOLIO ----------\n\n"
    )

    for stock in portfolio:

        report += (
            f"{stock}: "
            f"{portfolio[stock]} shares "
            f"(₹{stocks[stock]})\n"
        )

    report += (
        "\n---------- ACHIEVEMENTS ----------\n\n"
    )

    if achievements_unlocked:

        for achievement in achievements_unlocked:

            report += (
                f"- {achievement}\n"
            )

    else:

        report += "None\n"

    report += (
        "\n---------- TRANSACTION HISTORY ----------\n\n"
    )

    if transaction_history:

        for transaction in transaction_history:

            report += (
                transaction + "\n"
            )

    else:

        report += "No transactions\n"

    with open(
        "game_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    messagebox.showinfo(
        "Export Complete",
        "Professional report exported successfully."
    )

# ----------------------------
# Portfolio Allocation
# ----------------------------

def view_allocation():

    total_value = calculate_portfolio_value()

    if total_value == 0:

        messagebox.showinfo(
            "Allocation",
            "No stocks owned."
        )

        return

    text = "PORTFOLIO ALLOCATION\n\n"

    for stock in portfolio:

        value = (
            portfolio[stock]
            * stocks[stock]
        )

        percent = (
            value / total_value
        ) * 100

        text += (
            f"{stock}: "
            f"{percent:.1f}%\n"
        )

    messagebox.showinfo(
        "Allocation",
        text
    )

# ----------------------------
# Game Help
# ----------------------------

def view_help():

    help_window = tk.Toplevel(root)

    help_window.title("Game Rules")
    help_window.configure(bg="#0f172a")
    help_window.resizable(False, False)
    help_window.transient(root)
    help_window.grab_set()

    center_popup(
        help_window,
        root,
        760,
        560
    )

    tk.Label(
        help_window,
        text="📖 GAME GUIDE",
        font=("Segoe UI", 22, "bold"),
        fg="#38bdf8",
        bg="#0f172a"
    ).pack(
        pady=(18, 12)
    )

    content_frame = tk.Frame(
        help_window,
        bg="#1e293b"
    )

    content_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    scrollbar = ttk.Scrollbar(content_frame)

    help_text = tk.Text(
        content_frame,
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 11),
        wrap="word",
        relief="flat",
        padx=15,
        pady=15,
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(command=help_text.yview)

    help_text.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    help_text.insert(
        "1.0",
        """
STOCK MARKET SURVIVAL
==============================

🎯 GOAL

Reach ₹1,000,000 Net Worth
before Day 30.

──────────────────────────────

📈 HOW TO PLAY

• Buy stocks.

• Advance to the next day.

• Prices change every day.

• Market events affect prices.

• Receive dividends.

• Experience stock splits.

• Sell stocks to make profits.

──────────────────────────────

💀 GAME OVER

• Net Worth falls below ₹10,000.

OR

• Day 30 is completed.

──────────────────────────────

🏆 VICTORY

Reach ₹1,000,000 Net Worth
before Day 30.

──────────────────────────────

💡 TIPS

• Diversify your investments.

• Keep emergency cash.

• Buy during crashes.

• Sell after rallies.

• Watch the News Feed.

• Track your portfolio.

• Don't invest everything in one stock.

──────────────────────────────

Good luck and become the
Market Legend!
"""
    )

    help_text.config(state="disabled")

    footer = tk.Frame(
        help_window,
        bg="#0f172a"
    )

    footer.pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Button(
        footer,
        text="Close",
        command=help_window.destroy,
        bg="#2563eb",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=18
    ).pack(
        side="right"
    )

# ----------------------------
# Connect Quick Action Buttons
# ----------------------------

buy_stock_button.config(command=open_buy_popup)
sell_stock_button.config(command=open_sell_popup)
next_day_action_button.config(command=next_day)

save_action_button.config(command=save_game)
load_action_button.config(command=load_game)

portfolio_action_button.config(command=view_portfolio_summary)
history_action_button.config(command=view_transaction_history)

leaderboard_action_button.config(command=view_leaderboard)
statistics_action_button.config(command=view_statistics)

achievement_action_button.config(command=view_achievements)
help_action_button.config(command=view_help)

refresh_portfolio_table()

update_chart()

# Show all achievements in locked state when the game starts
update_achievement_display()

# ----------------------------
# Run App
# ----------------------------

root.mainloop()
