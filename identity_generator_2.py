import pandas as pd
import numpy as np

# Loading the data from files
firstnames_df = pd.read_excel('firstname_male.xlsx')
lastnames_df = pd.read_excel('lastname_male.xlsx')

# Calculate the total counts for first names and last names

total_firstnames = firstnames_df.iloc[:,2].sum()
total_lastnames = lastnames_df.iloc[:,1].sum()

firstnames_df['probability'] = firstnames_df.iloc[:,2] / total_firstnames
lastnames_df['probability'] = lastnames_df.iloc[:,1] / total_lastnames

def generate_name(firstnames_df, lastnames_df):
    firstname = np.random.choice(firstnames_df.iloc[:,0], p=firstnames_df['probability'])
    lastname = np.random.choice(lastnames_df.iloc[:,0], p=lastnames_df['probability'])
    return f"{firstname} {lastname}"

def generate_names_list(n, firstnames_df, lastnames_df):
    return [generate_name(firstnames_df, lastnames_df) for _ in range(n)]

# Example usage: Generate 10 random names
random_names = generate_names_list(10, firstnames_df, lastnames_df)
for name in random_names:
    print(name)
