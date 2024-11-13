import os
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from django.conf import settings

def Fa_value(site, interpolated_sa02):
    
    # TABLE 11.4-1 SITE COEFFICIENT, Fa
    Fatable = [
        [0.80, 0.80, 0.80, 0.80, 0.80],
        [1.00, 1.00, 1.00, 1.00, 1.00],
        [1.20, 1.20, 1.10, 1.00, 1.00],
        [1.60, 1.40, 1.20, 1.10, 1.00],
        [2.50, 1.70, 1.20, 0.90, 0.90]
    ]

    # Mapping of site rows and columns
    row_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    col_values = [0.25, 0.5, 0.75, 1, 1.25]

    # Check if the interpolated_sa02 value is None
    if interpolated_sa02 is None:
        raise ValueError(f"Invalid interpolated_sa02 value: {interpolated_sa02}. Interpolation failed.")
    
    # Find the row index for the site
    row_index = row_map.get(site.upper())
    if row_index is None:
        raise ValueError(f"Invalid site value: {site}. Choose from A, B, C, D, E.")

    # Boundary conditions for column
    if interpolated_sa02 <= 0.25:
        col_index = 0
        return Fatable[row_index][col_index]
    elif interpolated_sa02 >= 1.25:
        col_index = 4
        return Fatable[row_index][col_index]
    
    # Determine the two closest column indices for interpolation if in range
    for i in range(len(col_values) - 1):
        if col_values[i] <= interpolated_sa02 <= col_values[i + 1]:
            # Perform linear interpolation
            x0, x1 = col_values[i], col_values[i + 1]
            y0, y1 = Fatable[row_index][i], Fatable[row_index][i + 1]
            return y0 + (y1 - y0) * (interpolated_sa02 - x0) / (x1 - x0)



def Fv_value(site, interpolated_sa1):

    # TABLE 11.4-2 SITE COEFFICIENT, Fv
    Fvtable = [
        [0.80, 0.80, 0.80, 0.80, 0.80],
        [1.00, 1.00, 1.00, 1.00, 1.00],
        [1.70, 1.60, 1.50, 1.40, 1.30],
        [2.40, 2.00, 1.80, 1.60, 1.50],
        [3.50, 3.20, 2.80, 2.40, 2.40]
    ]

    # Mapping of site rows and columns
    row_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    col_values = [0.1, 0.2, 0.3, 0.4, 0.5]

    # Find the row index for the site
    row_index = row_map.get(site.upper())
    if row_index is None:
        raise ValueError(f"Invalid site value: {site}. Choose from A, B, C, D, E.")

    # Boundary conditions for column
    if interpolated_sa1 <= 0.1:
        col_index = 0
        return Fvtable[row_index][col_index]
    elif interpolated_sa1 >= 0.5:
        col_index = 4
        return Fvtable[row_index][col_index]
    
    # Determine the two closest column indices for interpolation if in range
    for i in range(len(col_values) - 1):
        if col_values[i] <= interpolated_sa1 <= col_values[i + 1]:
            # Perform linear interpolation
            x0, x1 = col_values[i], col_values[i + 1]
            y0, y1 = Fvtable[row_index][i], Fvtable[row_index][i + 1]
            return y0 + (y1 - y0) * (interpolated_sa1 - x0) / (x1 - x0)

def process_sa_pga_map(lat, lon, site):
    # Define the path to the CSV file
    csv_file_path = "C:/Users/Jedrek/Documents/GitHub/SHADEWebApp/myapp/data/points.csv"
    # csv_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'points.csv')
    
    # Load the points and additional data from the CSV file
    df = pd.read_csv(csv_file_path)
    points = df[['xcoord', 'ycoord']].values
    values_sa1 = df['Combined-SA1'].values
    values_sa02 = df['Combined-SA02'].values
    values_tl = df['TL'].values
    
    given_point = [lat, lon]
    
    # Perform interpolation to find the nearest values
    interpolated_sa1 = griddata(points, values_sa1, given_point, method='linear')
    interpolated_sa02 = griddata(points, values_sa02, given_point, method='linear')
    interpolated_tl = griddata(points, values_tl, given_point, method='nearest')
    
    # Handle potential NaN values in interpolation results
    if np.isnan(interpolated_sa1):
        interpolated_sa1 = None
    if np.isnan(interpolated_sa02):
        interpolated_sa02 = None
    if np.isnan(interpolated_tl):
        interpolated_tl = None
    Favalue = Fa_value(site, interpolated_sa02)
    Fvvalue = Fv_value(site, interpolated_sa1)
    SMS = Favalue * interpolated_sa02
    SM1 = Fvvalue * interpolated_sa1
    SDS = SMS * (2 / 3)
    SD1 = SM1 * (2/3)
    Ts = SD1 / SDS
    To = 0.2 * Ts
    
    print(lat)
    print(lon)
    print(site)
    print(interpolated_sa1)
    print(interpolated_sa02)
    print(interpolated_tl)
    print(Favalue)
    print(Fvvalue)
    print(SMS)
    print(SM1)
    print(SDS)
    print(SD1)
    print(Ts)
    print(To)


    return {
        'current_coord': given_point,
        'sa1': float(interpolated_sa1) if interpolated_sa1 is not None else None,
        'sa02': float(interpolated_sa02) if interpolated_sa02 is not None else None,
        'tl': float(interpolated_tl) if interpolated_tl is not None else None,
        'Fa': float(Favalue) if Favalue is not None else None,
        'Fv': float(Fvvalue) if Fvvalue is not None else None,
        'SMS': float(SMS) if SMS is not None else None,
        'SM1': float(SM1) if SM1 is not None else None,
        'SDS': float(SDS) if SDS is not None else None,
        'SD1': float(SD1) if SD1 is not None else None,
        'Ts': float(Ts) if Ts is not None else None,
        'To': float(To) if To is not None else None,
    }




# lat = 14.60388
# lon = 121.04986
# site = "D"
# process_sa_pga_map(lat, lon, site)
