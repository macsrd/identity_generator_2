import pandas as pd
import numpy as np
import random
import tkinter as tk
from tkinter import ttk
from random_pesel import RandomPESEL



# Function to load data from Excel and calculate probabilities
def load_data(firstname_file, lastname_file):
    try:
        firstnames_df = pd.read_excel(firstname_file)
        lastnames_df = pd.read_excel(lastname_file)
    except Exception as e:
        print(f"Error reading files: {e}")
        return None, None

    try:
        total_firstnames = firstnames_df.iloc[:,2].sum()
        total_lastnames = lastnames_df.iloc[:,1].sum()

        firstnames_df['probability'] = firstnames_df.iloc[:,2] / total_firstnames
        lastnames_df['probability'] = lastnames_df.iloc[:,1] / total_lastnames
    except KeyError as e:
        print(f"Error in data format: Missing expected column {e}")
        return None, None

    return firstnames_df, lastnames_df

# Function to generate a random combination of firstname and lastname with probability
def generate_name_with_probability(firstnames_df, lastnames_df):
    firstname = np.random.choice(firstnames_df.iloc[:,0], p=firstnames_df['probability'])
    lastname = np.random.choice(lastnames_df.iloc[:,0], p=lastnames_df['probability'])
    
    firstname_prob = firstnames_df[firstnames_df.iloc[:,0] == firstname]['probability'].values[0]
    lastname_prob = lastnames_df[lastnames_df.iloc[:,0] == lastname]['probability'].values[0]
    
    combined_prob = firstname_prob * lastname_prob
    
    return f"{firstname} {lastname}", combined_prob

# Load data for male and female names
female_firstnames_df, female_lastnames_df = load_data('firstname_female.xlsx', 'lastname_female.xlsx')
male_firstnames_df, male_lastnames_df = load_data('firstname_male.xlsx', 'lastname_male.xlsx')

# Check if data is loaded correctly
if female_firstnames_df is None or female_lastnames_df is None:
    print("Failed to load female names data.")
if male_firstnames_df is None or male_lastnames_df is None:
    print("Failed to load male names data.")

# Function to generate identity based on gender
def generate_identity(gender):
    if gender.lower() == 'female':
        name, probability = generate_name_with_probability(female_firstnames_df, female_lastnames_df)
        pesel = RandomPESEL().generate(gender='f')
    elif gender.lower() == 'male':
        name, probability = generate_name_with_probability(male_firstnames_df, male_lastnames_df)
        pesel = RandomPESEL().generate(gender='m')
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return name, probability, pesel

# Function to display generated identity in the GUI
def display_identity():
    gender = gender_var.get()
    try:
        random_name, probability, pesel = generate_identity(gender)
        result_label.config(text=f"Generated Name: {random_name}\nProbability: {probability * 100:.6f}%\nPESEL: {pesel}")
    except ValueError as e:
        result_label.config(text=f"Error: {e}")
    except TypeError as e:
        result_label.config(text=f"Error generating name: {e}")

# Create the tkinter GUI
root = tk.Tk()
root.title("Identity Generator")

# Gender selection
gender_var = tk.StringVar(value="male")
ttk.Label(root, text="Select Gender:").grid(column=0, row=0, padx=10, pady=10)
ttk.Radiobutton(root, text="Male", variable=gender_var, value="male").grid(column=1, row=0, padx=10, pady=10)
ttk.Radiobutton(root, text="Female", variable=gender_var, value="female").grid(column=2, row=0, padx=10, pady=10)

# Generate button
generate_button = ttk.Button(root, text="Generate Identity", command=display_identity)
generate_button.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

# Result display
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
