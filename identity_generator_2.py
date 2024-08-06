import pandas as pd
import numpy as np
from random_pesel import RandomPESEL


# Function loading data and calculating probability
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

# Function generating name and probability
def generate_name(firstnames_df, lastnames_df):
    firstname = np.random.choice(firstnames_df.iloc[:,0], p=firstnames_df['probability'])
    lastname = np.random.choice(lastnames_df.iloc[:,0], p=lastnames_df['probability'])

    firstname_prb = firstnames_df[firstnames_df.iloc[:,0] == firstname]['probability'].values[0]
    lastname_prb = lastnames_df[lastnames_df.iloc[:,0] == lastname]['probability'].values[0]

    combined_prob = firstname_prb * lastname_prb
    
    return f"{firstname} {lastname}", combined_prob

female_firstnames_df, female_lastnames_df = load_data('firstname_female.xlsx', 'lastname_female.xlsx')
male_firstnames_df, male_lastnames_df = load_data('firstname_male.xlsx', 'lastname_male.xlsx')



if female_firstnames_df is None or female_lastnames_df is None:
    print("Failed to load female names data.")
if male_firstnames_df is None or male_lastnames_df is None:
    print("Failed to load male names data.")

def generate_identity(gender):
    if gender.lower() == 'female':
        name, probability = generate_name(female_firstnames_df, female_lastnames_df)
        pesel = RandomPESEL().generate(gender='f')
    elif gender.lower() == 'male':
        name, probability = generate_name(male_firstnames_df, male_lastnames_df)
        pesel = RandomPESEL().generate(gender='m')
    else:
         raise ValueError("Gender must be 'male' or 'female'")    
    
    return name, probability, pesel

gender = input("Enter the gender for the identity (male/female): ").strip()
try:
    random_name, probability, pesel = generate_identity(gender)
    print(f"Generated Name: {random_name}")
    print(f"Generated Name Probability: {probability* 100:.6f}%")
    print(f"PESEL Number: {pesel}")
except ValueError as e:
    print(e)
except TypeError as e:
    print(f"Error generating name: {e}")
