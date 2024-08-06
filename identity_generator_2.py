import pandas as pd
import numpy as np
from random_pesel import RandomPESEL

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

    firstname_prb = firstnames_df[firstnames_df.iloc[:,0] == firstname]['probability'].values[0]
    lastname_prb = lastnames_df[lastnames_df.iloc[:,0] == lastname]['probability'].values[0]

    combined_prob = firstname_prb * lastname_prb

    pesel = RandomPESEL()
    pesel = pesel.generate(gender='m')
    
    return f"{firstname} {lastname}", combined_prob, pesel

random_name, probability, pesel = generate_name(firstnames_df, lastnames_df)

print(f"Generated Name: {random_name}")
print(f"Generated Name Probability: {probability* 100:.6f}%")
print(f"PESEL Number: {pesel}")
