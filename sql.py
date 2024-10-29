import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

# Establish connection to SQL Server
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost;"  # Replace 'localhost' with your server name if different
    "Database=recipe_management;"  # The database created in SSMS
    "UID=sa;"  # Replace with your SQL Server username
    "PWD=Gurpreet3443B"  # Replace with your SQL Server password
)
cursor = conn.cursor()

# Function to add a new recipe
def add_recipe():
    recipe_name = recipe_entry.get().strip().lower()
    ingredients = ingredients_entry.get().strip().lower()
    
    try:
        cursor.execute("INSERT INTO recipes (name, ingredients) VALUES (?, ?)", (recipe_name, ingredients))
        conn.commit()
        messagebox.showinfo("Success", f"Recipe '{recipe_name.title()}' added successfully.", icon='info')
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", f"Recipe '{recipe_name.title()}' already exists.")

# Function to view all recipes
def view_recipes():
    cursor.execute("SELECT name, ingredients FROM recipes")
    recipes_data = cursor.fetchall()
    recipe_list = "\n".join(f"{name.title()}: {ingredients}" for name, ingredients in recipes_data)
    messagebox.showinfo("Recipes", recipe_list or "No recipes available.", icon='info')

# Function to add ingredients to pantry
def add_to_pantry():
    new_ingredients = pantry_entry.get().strip().lower().split(',')
    new_ingredients = [ingredient.strip() for ingredient in new_ingredients]

    for ingredient in new_ingredients:
        try:
            cursor.execute("INSERT INTO pantry (ingredient) VALUES (?)", (ingredient,))
        except pyodbc.IntegrityError:
            pass  # Ignore duplicates
    conn.commit()
    messagebox.showinfo("Success", f"Ingredients '{', '.join(new_ingredients)}' added to pantry.", icon='info')

# Function to check if a recipe can be made
def check_recipe():
    recipe_name = check_entry.get().strip().lower()
    cursor.execute("SELECT ingredients FROM recipes WHERE name = ?", (recipe_name,))
    result = cursor.fetchone()
    
    if result is None:
        messagebox.showerror("Error", f"No recipe found with the name '{recipe_name}'.")
        return

    recipe_ingredients = set(result[0].split(', '))
    cursor.execute("SELECT ingredient FROM pantry")
    pantry_contents = set(row[0] for row in cursor.fetchall())
    missing_ingredients = recipe_ingredients - pantry_contents

    if not missing_ingredients:
        messagebox.showinfo("Success", f"You have all the ingredients to make '{recipe_name.title()}'.", icon='info')
    else:
        messagebox.showwarning("Missing Ingredients", f"You're missing: {', '.join(missing_ingredients)}.")

# Function to view pantry contents
def view_pantry():
    cursor.execute("SELECT ingredient FROM pantry")
    pantry_items = [row[0] for row in cursor.fetchall()]
    pantry_contents = ", ".join(pantry_items) or "Your pantry is empty."
    messagebox.showinfo("Pantry Contents", pantry_contents, icon='info')

# Set up the tkinter window
root = tk.Tk()
root.title("Recipe Book with Ingredient Checker")
root.geometry("400x500")  # Set window size
root.configure(bg="#f2f2f2")  # Background color

# Create a frame for better organization
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

# Styling for labels and buttons
label_style = {'bg': '#f2f2f2', 'font': ('Arial', 12)}
button_style = {'font': ('Arial', 10), 'bg': '#4CAF50', 'fg': 'white'}

# Labels and entries for adding a recipe
tk.Label(frame, text="Add Recipe", **label_style).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(frame, text="Recipe Name:", **label_style).grid(row=1, column=0, sticky="e")
recipe_entry = tk.Entry(frame, font=('Arial', 12))
recipe_entry.grid(row=1, column=1, padx=10)

tk.Label(frame, text="Ingredients (comma-separated):", **label_style).grid(row=2, column=0, sticky="e")
ingredients_entry = tk.Entry(frame, font=('Arial', 12))
ingredients_entry.grid(row=2, column=1, padx=10)

# Add recipe button
add_recipe_btn = tk.Button(frame, text="Add Recipe", command=add_recipe, **button_style)
add_recipe_btn.grid(row=3, column=0, columnspan=2, pady=5)

# Button to view all recipes
view_recipes_btn = tk.Button(frame, text="View All Recipes", command=view_recipes, **button_style)
view_recipes_btn.grid(row=4, column=0, columnspan=2, pady=5)

# Label and entry for adding to pantry
tk.Label(frame, text="Add to Pantry", **label_style).grid(row=5, column=0, columnspan=2, pady=5)
tk.Label(frame, text="Ingredients (comma-separated):", **label_style).grid(row=6, column=0, sticky="e")
pantry_entry = tk.Entry(frame, font=('Arial', 12))
pantry_entry.grid(row=6, column=1, padx=10)

# Add to pantry button
add_pantry_btn = tk.Button(frame, text="Add to Pantry", command=add_to_pantry, **button_style)
add_pantry_btn.grid(row=7, column=0, columnspan=2, pady=5)

# Button to view pantry contents
view_pantry_btn = tk.Button(frame, text="View Pantry", command=view_pantry, **button_style)
view_pantry_btn.grid(row=8, column=0, columnspan=2, pady=5)

# Label and entry for checking a recipe
tk.Label(frame, text="Check Recipe", **label_style).grid(row=9, column=0, columnspan=2, pady=5)
tk.Label(frame, text="Recipe Name:", **label_style).grid(row=10, column=0, sticky="e")
check_entry = tk.Entry(frame, font=('Arial', 12))
check_entry.grid(row=10, column=1, padx=10)

# Check recipe button
check_recipe_btn = tk.Button(frame, text="Check Recipe", command=check_recipe, **button_style)
check_recipe_btn.grid(row=11, column=0, columnspan=2, pady=5)

# Exit button
exit_btn = tk.Button(frame, text="Exit", command=root.quit, **button_style)
exit_btn.grid(row=12, column=0, columnspan=2, pady=10)

# Run the tkinter app
root.mainloop()
