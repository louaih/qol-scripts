import tkinter as tk
from datetime import datetime

# Function to calculate and update earnings
def update_earnings():
    current_date = datetime.now()
    time_difference = current_date - start_date
    elapsed_seconds = time_difference.total_seconds()
    earnings = initial_balance * (1 + apy) ** (elapsed_seconds / (365 * 24 * 60 * 60)) - initial_balance
    result_label.config(text=f"Earnings: ${earnings:.8f}", font=("Helvetica", 16))  # Increase font size
    window.after(100, update_earnings)  # Update every second

# Function to set initial_balance, apy, and start_date from user input
def calculate_earnings():
    global initial_balance, apy, start_date
    try:
        initial_balance = float(initial_balance_entry.get())
        apy = float(apy_entry.get()) / 100  # Convert percentage to decimal
        start_date_str = start_date_entry.get()
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
        update_earnings()
    except ValueError:
        result_label.config(text="Invalid input. Please enter valid numbers and a valid start date (MM/DD/YYYY).")

# Create the main window
window = tk.Tk()
window.title("Earnings Calculator")

# Create and place input widgets
initial_balance_label = tk.Label(window, text="Initial Balance:", font=("Helvetica", 14))  # Increase font size
initial_balance_label.pack()

initial_balance_entry = tk.Entry(window)
initial_balance_entry.pack()

apy_label = tk.Label(window, text="APY (%):", font=("Helvetica", 14))  # Increase font size
apy_label.pack()

apy_entry = tk.Entry(window)
apy_entry.pack()

start_date_label = tk.Label(window, text="Start Date (MM/DD/YYYY):", font=("Helvetica", 14))  # Increase font size
start_date_label.pack()

# Set the default start date to the beginning of the current year
current_year = datetime.now().year
default_start_date = datetime(current_year, 1, 1)
start_date_entry = tk.Entry(window)
start_date_entry.insert(0, default_start_date.strftime("%m/%d/%Y"))
start_date_entry.pack()

calculate_button = tk.Button(window, text="Calculate Earnings", command=calculate_earnings, font=("Helvetica", 14))  # Increase font size
calculate_button.pack()

result_label = tk.Label(window, text="Earnings: $0.00000000", font=("Helvetica", 16))  # Increase font size
result_label.pack()

# Initialize global variables
initial_balance = 0.0
apy = 0.0
start_date = default_start_date

# Start the Tkinter event loop
window.after(1000, update_earnings)  # Initial update after 1 second
window.mainloop()
