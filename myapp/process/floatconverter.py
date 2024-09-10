import pandas as pd

# Read the Excel file
file_path = r"C:/Users/shade/Downloads/SHADE App/demos - Copy/Catalog Declustering Tool/For_Validation.xlsx"
df = pd.read_excel(file_path)

# Convert Year, Month, Day, Hour, Minute, and Second columns to floats with 3 decimals
df['Year'] = df['Year'].astype(float).round(3)
df['Month'] = df['Month'].astype(float).round(3)
df['Day'] = df['Day'].astype(float).round(3)
df['Hour'] = df['Hour'].astype(float).round(3)
df['Minute'] = df['Minute'].astype(float).round(3)
df['Second'] = df['Second'].astype(float).round(3)

# Write the modified DataFrame back to the same Excel file
df.to_excel(file_path, index=False)
