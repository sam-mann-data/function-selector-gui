import tkinter as tk
from tkinter import ttk, simpledialog
import subprocess

# Mapping of flavors to script filenames
flavor_map = {
    "Pink": "pink.py",
    "Blue": "blue.py",
    "Green": "green.py"
}

selected_flavor = None  # Stores the user's chosen flavor
num_cupcakes = None  # Stores the entered number

def select_flavor(event):
    """Update selected_flavor when the user chooses a flavor from the dropdown."""
    global selected_flavor
    selected_flavor = flavor_map[flavor_var.get()]
    flavor_label.config(text=f"Flavor Selected: {flavor_var.get()}")

def enter_num():
    """Prompt user to enter the number of cupcakes."""
    global num_cupcakes
    num = simpledialog.askinteger("Enter Number", "How many cupcakes do you want?")
    
    if num and num > 0:
        num_cupcakes = num
        num_label.config(text=f"Number Entered: {num}")
    else:
        num_label.config(text="Invalid number! Try again.")

def update_script_and_run():
    """Modify the selected script to update numcake and run it."""
    if not selected_flavor or num_cupcakes is None:
        output_label.config(text="Error: Select a flavor and enter a number first!")
        return
    
    try:
        # Read the selected flavor script and update numcake
        with open(selected_flavor, "r") as file:
            lines = file.readlines()

        # Modify the numcake variable
        for i, line in enumerate(lines):
            if line.startswith("numcake"):
                lines[i] = f"numcake = {num_cupcakes}\n"

        # Write the modified content back to the file
        with open(selected_flavor, "w") as file:
            file.writelines(lines)

        # Run the updated script
        subprocess.run(["python", selected_flavor])

        output_label.config(text=f"Successfully made {num_cupcakes} {flavor_var.get()} cupcakes!")
    except Exception as e:
        output_label.config(text=f"Error: {e}")

# Create GUI
root = tk.Tk()
root.title("Cupcake Maker")

# Flavor selection dropdown
ttk.Label(root, text="Select cupcake flavor:").grid(row=0, column=0, padx=10, pady=5)
flavor_var = tk.StringVar()
flavor_dropdown = ttk.Combobox(root, textvariable=flavor_var, values=list(flavor_map.keys()), state="readonly")
flavor_dropdown.grid(row=0, column=1, padx=10, pady=5)
flavor_dropdown.set("Select...")  # Default value
flavor_dropdown.bind("<<ComboboxSelected>>", select_flavor)  # Bind selection event

# Label to display selected flavor
flavor_label = ttk.Label(root, text="No flavor selected")
flavor_label.grid(row=0, column=2, padx=10, pady=5)

# Number of cupcakes input button
ttk.Button(root, text="Enter Number", command=enter_num).grid(row=1, column=0, padx=10, pady=5)
num_label = ttk.Label(root, text="No number entered")
num_label.grid(row=1, column=1, padx=10, pady=5)

# Manufacture button
ttk.Button(root, text="Make Cupcakes", command=update_script_and_run).grid(row=2, columnspan=3, pady=10)

# Output label for messages
output_label = ttk.Label(root, text="", foreground="blue")
output_label.grid(row=3, columnspan=3, padx=10, pady=5)

root.mainloop()
