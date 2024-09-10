#Import necessary packages
import pandas as pd
import numpy as np
import os
from shapely.geometry import Point, Polygon


def assign_depth(latitude, longitude):
    # Define the polygon with coordinates
    polygon = Polygon([(14.8, 120.88), (14.8, 121.16), (14.3, 121.16), (14.3, 120.88)])
    
    # Create a point object for the given latitude and longitude
    point = Point(latitude, longitude)
    
    # Check if the point falls within the polygon
    if polygon.contains(point):
        return 1  # Depth is 1 km
    else:
        return 5  # Depth is 5 km



def clean_and_process_data(input_file_path, output_file_path):

    #List all files in input directory
    excel_file_list = os.listdir(input_file_path)

    #Create dataframe
    df = pd.DataFrame()

    print("Combining the following raw data files into a single catalogue.")

    #Stack all rows into a single file
    for excel_files in excel_file_list:

    #check for .xlsx suffix files only
        if excel_files.endswith(".xlsx"):

            print(excel_files)
            #create a new dataframe to read/open each Excel file from the list of files created above
            df1 = pd.read_excel(input_file_path + excel_files)
            
            #append each file into the original empty dataframe
            df = pd.concat([df,df1], ignore_index=True)

    #Create a new file for the stacked catalogue with .xslx extension
    df.to_excel(output_file_path + "Stacked_Catalogue.xlsx", index=False)

    #print all the files stored in the folder, after defining the list
    print(excel_file_list)

    #Remove Spaces in column Headers
    df.columns = df.columns.str.strip()

    #Remove spaces in column TYPE
    df['TYPE'] = df['TYPE'].str.strip()

    

    #Strip all whitespaces from whole dataframe
    df = df.apply(lambda x: x.strip() if isinstance(x, str) else x)

    #indicate needed columns
    columns_to_keep = ['EVENTID', 'AUTHOR', 'DATE', 'TIME', 'LAT', 'LON', 'DEPTH', 'TYPE', 'MAG']
    #drop all columns except stated above
    df.drop(df.columns.difference(columns_to_keep), axis=1, inplace=True)

    df['AUTHOR'] = df['AUTHOR'].fillna('Unknown').astype(str)
    df['AUTHOR'] = df['AUTHOR'].astype(str)
    print(df['AUTHOR'].apply(lambda x: isinstance(x, str)).all())
    print(df.dtypes)

    # Make everything uppercase, to make all data uniform
    df = df.apply(lambda x: x.upper() if isinstance(x, str) else x)

    # Filter rows where 'TYPE' is 'MB', 'MS', 'ML' or 'MW'
    valid_types = ['MB', 'MS', 'ML', 'MW']
    filtered_df = df[df['TYPE'].isin(['MB', 'ML', 'MS', 'MW'])]

    # Reset the DataFrame index after filtering rows
    df.reset_index(drop=True, inplace=True)
    df['LAT'] = df['LAT'].astype(float)
    df['LON'] = df['LON'].astype(float)

    # Remove coordinates outside PH
    df = df[(df['LAT'] >= -1.2) & (df['LAT'] <= 24.2)]
    df = df[(df['LON'] >= 112.7) & (df['LON'] <= 134.2)]

    # Reset the DataFrame index after removing rows
    df.reset_index(drop=True, inplace=True)
    after_rows_count = ("After: " + str(len(df.index)))
    after_rows_count
    #add columns
    df[['MAGCONV','TClass']] = ''

    # # Transfer MAG data based on TYPE column
    # conditions = {
    #     'ML': 'mL',
    #     'MB': 'mb',
    #     'MS': 'ms',
    #     'MW': 'mw'
    # }  

    # for type_value, target_column in conditions.items():
    #     mask = df['TYPE'] == type_value
    #     df.loc[mask, target_column] = df.loc[mask, 'MAG']

    # #Remove columns
    # columns_to_drop = ['MAG']
    # df.drop(columns=columns_to_drop, inplace=True)

    # Function to categorize depth
    def categorize_depth(depth):
        if depth == "":
            depth = 0
        depth = float(depth)

        if pd.isnull(depth) or (isinstance(depth, str) and depth.strip() == ''):
            return 'Crustal'
        depth = float(depth)  # changed int to float
        if depth <= 25:
            return 'Crustal'
        elif depth <= 60:
            return 'Interface'
        else:
            return 'Intraslab'

    # Convert 'DEPTH' column to int or handle NaN/empty values
    df['DEPTH'] = df['DEPTH'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['DEPTH'] = df['DEPTH'].fillna(0)

    # Apply the assign_depth function to each row to get the depth value
    df['DEPTH'] = df.apply(lambda row: assign_depth(row['LAT'], row['LON']) if pd.isnull(row['DEPTH']) or (isinstance(row['DEPTH'], str) and row['DEPTH'].strip() == '0') else row['DEPTH'], axis=1)

    # Apply categorization to each row
    df['TClass'] = df['DEPTH'].apply(categorize_depth)

    # TClass_counts = df['TClass'].value_counts()
    def calculate_MAGCONV(df):
        # Ensure 'MAG' column is numeric
        df['MAG'] = pd.to_numeric(df['MAG'], errors='coerce').fillna(0).astype(float)
        def isc_bulletin(row):
            if row['TYPE'] == 'MB':
                return 1.084 * row['MAG'] - 0.142
            elif row['TYPE'] == 'MS':
                if row['MAG'] > 6.0:
                    return 0.616 * row['MAG'] + 2.369
                else:
                    return 0.994 * row['MAG'] + 0.100
            else:
                return row['MAG']

        def usgs_neic(row):
            if row['TYPE'] == 'MB':
                return 1.159 * row['MAG'] - 0.659
            elif row['TYPE'] == 'MS':
                if row['MAG'] > 6.47:
                    return 1.005 * row['MAG'] - 0.026
                else:
                    return 0.723 * row['MAG'] + 1.798
            else:
                return row['MAG']

        def neid(row):
            if row['TYPE'] == 'MB':
                return 0.964 * row['MAG'] + 0.248
            else:
                return row['MAG']

        def phivolcs(row):
            if row['TYPE'] == 'MB':
                return 0.998 * row['MAG'] - 0.305
            elif row['TYPE'] == 'ML':
                return 0.979 * row['MAG'] + 0.711
            elif row['TYPE'] == 'MS':
                if row['MAG'] > 5.8:
                    return 1.407 * row['MAG'] - 2.937
                else:
                    return 0.407 * row['MAG'] + 3.225
            else:
                return row['MAG']

        # Define conditions and choices
        conditions = [
            (df['AUTHOR'] == 'ISC_BULLETIN') & (df['TYPE'] == 'MB'),
            (df['AUTHOR'] == 'ISC_BULLETIN') & (df['TYPE'] == 'MS'),
            (df['AUTHOR'] == 'USGS_NEIC') & (df['TYPE'] == 'MB'),
            (df['AUTHOR'] == 'USGS_NEIC') & (df['TYPE'] == 'MS'),
            (df['AUTHOR'] == 'NEID') & (df['TYPE'] == 'MB'),
            (df['AUTHOR'] == 'PHIVOLCS') & (df['TYPE'] == 'MB'),
            (df['AUTHOR'] == 'PHIVOLCS') & (df['TYPE'] == 'ML'),
            (df['AUTHOR'] == 'PHIVOLCS') & (df['TYPE'] == 'MS')
        ]
        choices = [
            df.apply(isc_bulletin, axis=1),
            df.apply(isc_bulletin, axis=1),
            df.apply(usgs_neic, axis=1),
            df.apply(usgs_neic, axis=1),
            df.apply(neid, axis=1),
            df.apply(phivolcs, axis=1),
            df.apply(phivolcs, axis=1),
            df.apply(phivolcs, axis=1)
        ]
        df['MAGCONV'] = np.select(conditions, choices, default=df['MAG'])
        return df
    # print("Unique values in 'AUTHOR':", df['AUTHOR'].unique())
    df=calculate_MAGCONV(df)

    df = df[df['MAGCONV'] != 0]

    # Split 'Time' into 'Hour', 'Minute', and 'Second' columns
    df[['Hour', 'Minute', 'Second']] = df['TIME'].str.split(':', expand=True)

    # Extract only the integer part of the 'Second' column
    df['Second'] = df['Second'].str.split('.').str[0]

    # Replace empty strings with 0 in the 'Second' column
    df['Second'] = df['Second'].replace('', '0')

    # Convert 'Hour', 'Minute', and 'Second' columns to integers
    df[['Hour', 'Minute', 'Second']] = df[['Hour', 'Minute', 'Second']].fillna(0).astype(int)

    df = df.drop(columns=['TIME'])

    # Concatenate whole row into an additional column named 'Concatenated'
    df['Concatenated'] = df.apply(lambda row: '|'.join(row.astype(str)), axis=1)

    # Drop duplicates based on the 'Concatenated' column
    df.drop_duplicates(subset='Concatenated', keep='first', inplace=True)

    # Drop the 'Concatenated' column as it's no longer needed
    df.drop(columns=['Concatenated'], inplace=True)

    # Extract the first 10 characters from the 'DATE' column
    df['DATE'] = df['DATE'].astype(str)
    df['DATE'] = df['DATE'].str[0:11]
    df['DATE'] = df['DATE'].str.replace('/', '-')

    # Assuming 'Date' column is in the format 'DD-MM-YYYY'
    df[['Year', 'Month', 'Day']] = df['DATE'].str.split('-', expand=True).astype(float)

    df = df[['AUTHOR', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'LAT', 'LON', 'DEPTH', 'MAGCONV', 'TClass']]
    df.rename(columns={'MAGCoNV': 'magW'}, inplace=True)
    df = df.dropna(subset=['DEPTH']).query("DEPTH != 0")

    columns_to_replace = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
    df[columns_to_replace] = df[columns_to_replace].fillna(0)
    df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']] = df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']]

    df['Year'] = df['Year'].astype(float).round(3)
    df['Month'] = df['Month'].astype(float).clip(lower=1, upper=12).round(3)
    df['Day'] = df['Day'].astype(float).clip(lower=1, upper=31).round(3)
    df['Hour'] = df['Hour'].astype(float).clip(lower=0, upper=23).round(3)
    df['Minute'] = df['Minute'].astype(float).clip(lower=0, upper=59).round(3)
    df['Second'] = df['Second'].astype(float).clip(lower=0, upper=59).round(3)

    df.to_excel(output_file_path+"For_Validation.xlsx")

    print("Cleaning Done")

    return df

# clean_and_process_data(input_file_path, output_file_path)