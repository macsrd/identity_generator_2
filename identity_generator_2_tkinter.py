import pandas as pd
import numpy as np
import random
import tkinter as tk
from tkinter import ttk
from random_pesel import RandomPESEL



# Function to load data from files and calculate probability
def load_data(firstname_file, lastname_file, secondname_file):
    try:
        firstnames_df = pd.read_excel(firstname_file)
        lastnames_df = pd.read_excel(lastname_file)
        secondnames_df = pd.read_csv(secondname_file) if secondname_file else None
    except Exception as e:
        print(f"Error reading files: {e}")
        return None, None, None

    try:
        total_firstnames = firstnames_df.iloc[:,2].sum()
        total_lastnames = lastnames_df.iloc[:,1].sum()

        firstnames_df['probability'] = firstnames_df.iloc[:,2] / total_firstnames
        lastnames_df['probability'] = lastnames_df.iloc[:,1] / total_lastnames

        if secondnames_df is not None:
            total_secondnames = secondnames_df.iloc[:, 2].sum()
            secondnames_df['probability'] = secondnames_df.iloc[:, 2] / total_secondnames
    except KeyError as e:
        print(f"Error in data format: Missing expected column {e}")
        return None, None, None

    return firstnames_df, lastnames_df, secondnames_df

# Function to generate random fullnames and probability
def generate_name_with_probability(firstnames_df, lastnames_df, secondnames_df=None, include_secondname=False):
    firstname = np.random.choice(firstnames_df.iloc[:,0], p=firstnames_df['probability'])
    lastname = np.random.choice(lastnames_df.iloc[:,0], p=lastnames_df['probability'])

    if include_secondname and secondnames_df is not None:
        secondname = np.random.choice(secondnames_df.iloc[:, 0], p=secondnames_df['probability'])
        fullname = f"{firstname} {secondname} {lastname}"
        secondname_prob = secondnames_df[secondnames_df.iloc[:, 0] == secondname]['probability'].values[0]
        combined_prob = firstnames_df[firstnames_df.iloc[:, 0] == firstname]['probability'].values[0] * \
                        secondname_prob * \
                        lastnames_df[lastnames_df.iloc[:, 0] == lastname]['probability'].values[0]

    
    else:
        fullname = f"{firstname} {lastname}"
        combined_prob = firstnames_df[firstnames_df.iloc[:, 0] == firstname]['probability'].values[0] * \
                        lastnames_df[lastnames_df.iloc[:, 0] == lastname]['probability'].values[0]
    
    return fullname, combined_prob

# Loading files
female_firstnames_df, female_lastnames_df, female_secondnames_df = load_data(
    'db/firstname_female.xlsx', 'db/lastname_female.xlsx', 'db/secondname_female.csv'
)
male_firstnames_df, male_lastnames_df, male_secondnames_df = load_data(
    'db/firstname_male.xlsx', 'db/lastname_male.xlsx', 'db/secondname_male.csv'
)

# Checking if files were loaded correctly
if female_firstnames_df is None or female_lastnames_df is None:
    print("Failed to load female names data.")
if male_firstnames_df is None or male_lastnames_df is None:
    print("Failed to load male names data.")

# Function generating identity basing on gender and optional secondname
def generate_identity(gender, include_secondname):
    if gender.lower() == 'female':
        name, probability = generate_name_with_probability(female_firstnames_df, female_lastnames_df, female_secondnames_df, include_secondname)
        pesel = RandomPESEL().generate(gender='f')
    elif gender.lower() == 'male':
        name, probability = generate_name_with_probability(male_firstnames_df, male_lastnames_df, male_secondnames_df, include_secondname)
        pesel = RandomPESEL().generate(gender='m')
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return name, probability, pesel

# Function displaying identity in GUI (Tkinter)
def display_identity():
    gender = gender_var.get()
    include_secondname = include_secondname_var.get() == 1
    try:
        random_name, probability, pesel = generate_identity(gender, include_secondname)
        result_label.config(text=f"Generated Name: {random_name}\nProbability: {probability * 100:.6f}%\nPESEL: {pesel}")
    except ValueError as e:
        result_label.config(text=f"Error: {e}")
    except TypeError as e:
        result_label.config(text=f"Error generating name: {e}")

# Creating Tkinter GUI
root = tk.Tk()
root.title("Identity Generator")

# Selecting Gender
gender_var = tk.StringVar(value="male")
ttk.Label(root, text="Select Gender:").grid(column=0, row=0, padx=10, pady=10)
ttk.Radiobutton(root, text="Male", variable=gender_var, value="male").grid(column=1, row=0, padx=10, pady=10)
ttk.Radiobutton(root, text="Female", variable=gender_var, value="female").grid(column=2, row=0, padx=10, pady=10)

# Including secondname
include_secondname_var = tk.IntVar(value=0)
ttk.Checkbutton(root, text="Include Second Name", variable=include_secondname_var).grid(column=0, row=1, columnspan=3, padx=10, pady=10)

# Defining Generate button
generate_button = ttk.Button(root, text="Generate Identity", command=display_identity)
generate_button.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

# Displaying results
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

# Starting GUI loop
root.mainloop()