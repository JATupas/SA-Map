import os
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from django.conf import settings
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def Fa_value(site, interpolated_sa02, fainput):
    
    # TABLE 11.4-1 SITE COEFFICIENT, Fa
    Fatable = [
        [0.80, 0.80, 0.80, 0.80, 0.80],
        [1.00, 1.00, 1.00, 1.00, 1.00],
        [1.20, 1.20, 1.10, 1.00, 1.00],
        [1.60, 1.40, 1.20, 1.10, 1.00],
        [2.50, 1.70, 1.20, 0.90, 0.90],
        [fainput,fainput,fainput,fainput,fainput]
    ]

    # Mapping of site rows and columns
    row_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
    col_values = [0.25, 0.5, 0.75, 1, 1.25]

    # Check if the interpolated_sa02 value is None
    if interpolated_sa02 is None:
        raise ValueError(f"Invalid interpolated_sa02 value: {interpolated_sa02}. Interpolation failed.")
    
    # Find the row index for the site
    row_index = row_map.get(site.upper())
    if row_index is None:
        raise ValueError(f"Invalid site value: {site}. Choose from A, B, C, D, E, F.")

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



def Fv_value(site, interpolated_sa1, fvinput):

    # TABLE 11.4-2 SITE COEFFICIENT, Fv
    Fvtable = [
        [0.80, 0.80, 0.80, 0.80, 0.80],
        [1.00, 1.00, 1.00, 1.00, 1.00],
        [1.70, 1.60, 1.50, 1.40, 1.30],
        [2.40, 2.00, 1.80, 1.60, 1.50],
        [3.50, 3.20, 2.80, 2.40, 2.40],
        [fvinput,fvinput,fvinput,fvinput,fvinput]
    ]

    # Mapping of site rows and columns
    row_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
    col_values = [0.1, 0.2, 0.3, 0.4, 0.5]

    # Find the row index for the site
    row_index = row_map.get(site.upper())
    if row_index is None:
        raise ValueError(f"Invalid site value: {site}. Choose from A, B, C, D, E, F.")

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
        
def load_polygon_data_from_csv():
    # Path to the CSV file
    # tl_file_path = "C:/Users/shade/ShadeApp/SHADEWebApp/myapp/data/TL_vertices.csv"
    tl_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'TL_vertices.csv')
    
    # Read the CSV into a DataFrame
    tl_df = pd.read_csv(tl_file_path)
    
    # Assuming that each polygon has multiple rows with same polygon_id (assuming polygon_id is the same for each polygon)
    polygon_data = {}
    
    # Group by polygon_id to collect coordinates for each polygon
    for polygon_id, group in tl_df.groupby('polygon_id'):
        # Extract the coordinates (Latitude, Longitude)
        coordinates = list(zip(group['Longitude'], group['Latitude']))  # (Longitude, Latitude)
        # Get the TL value for the polygon (assuming it's the same for all rows of the same polygon)
        tl_value = group['TL'].iloc[0]  
        # Add the polygon's coordinates and TL value to the dictionary
        polygon_data[polygon_id] = (coordinates, tl_value)
    
    return polygon_data

def get_tl_value_from_polygon(lat, lon, polygon_data):
    point = Point(lon, lat)  # Create a shapely Point object from lat/lon
    
    for polygon_id, (polygon_coords, tl_value) in polygon_data.items():
        polygon = Polygon(polygon_coords)  # Create Polygon from coordinates
        if polygon.contains(point):  # Check if the point is inside the polygon
            return tl_value  # Return the TL value for the polygon containing the point
    
    return 0  # Return None if no polygon contains the point

def process_sa_pga_map(lat, lon, site, fainput, fvinput):
    plt.close('all')   
    image_base64 = None
    # Define the path to the CSV file
    # data_file_path = "C:/Users/shade/ShadeApp/SHADEWebApp/myapp/data/points.csv"
    data_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'points.csv')
    
    
    # Load the points and additional data from the CSV file
    df = pd.read_csv(data_file_path)
    points = df[['xcoord', 'ycoord']].values
    values_sa1 = df['Combined-SA1'].values
    values_sa02 = df['Combined-SA02'].values
    given_point = [lat, lon]
    
    # Perform interpolation to find the nearest values
    interpolated_sa1 = griddata(points, values_sa1, given_point, method='linear')
    interpolated_sa02 = griddata(points, values_sa02, given_point, method='linear')

    polygon_data = load_polygon_data_from_csv()
    interpolated_tl = get_tl_value_from_polygon(lat, lon, polygon_data)
    
    # Handle potential NaN values in interpolation results
    if np.isnan(interpolated_sa1):
        interpolated_sa1 = None
    if np.isnan(interpolated_sa02):
        interpolated_sa02 = None
    if np.isnan(interpolated_tl):
        interpolated_tl = None
    Favalue = Fa_value(site, interpolated_sa02, fainput)
    Fvvalue = Fv_value(site, interpolated_sa1, fvinput)
    SMS = Favalue * interpolated_sa02
    SM1 = Fvvalue * interpolated_sa1
    SDS = SMS * (2 / 3)
    SD1 = SM1 * (2/3)
    Ts = SD1 / SDS
    To = 0.2 * Ts
    
    # Create initial dataframe
    df = pd.DataFrame({
        'Period': range(18)  # Period from 0 to 16
    })

    # Add additional points (To, Ts)
    df_additional = pd.DataFrame({
        'Period': [0.2, To, Ts]
    })

    # Concatenate and sort the DataFrame
    df = pd.concat([df, df_additional]).sort_values(by='Period').reset_index(drop=True)

    # Initialize the SA column
    df['SA'] = None

    # Define the function to apply conditions
    def calculate_sa(row):
        period = row['Period']
        if period < To:
            return SDS * (0.4 + (0.6 * (period / To)))
        elif To <= period <= Ts:
            return SDS
        elif Ts < period <= interpolated_tl:
            return SD1 / period
        elif period > interpolated_tl:
            return (SD1 * interpolated_tl) / (period ** 2)
        return None  # Default case (optional)

    # Apply the function to the DataFrame
    df['SA'] = df.apply(calculate_sa, axis=1)

    #Clear previous plots
    plt.clf()

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(df['Period'], df['SA'], color='blue', marker='o', markersize=6, label="Design Spectrum")

    # Ensure interpolated_tl is a scalar (check if it's an int or float, even if it's numpy.int64)
    if isinstance(interpolated_tl, (np.ndarray, np.generic)):
         interpolated_tl = interpolated_tl.item() 

    if isinstance(interpolated_tl, (int, float)):
        interpolated_point = df.loc[df['Period'] == interpolated_tl]
        if not interpolated_point.empty:
            # Plot the interpolated point in orange
            plt.scatter(interpolated_point['Period'], interpolated_point['SA'], color='orange', s=100, label='Tₗ', zorder=2)
        else:
            print(f"Warning: interpolated_tl value {interpolated_tl} not found in 'Period' column.")
    else:
        print(f"Error: interpolated_tl is not a scalar value. It is of type {type(interpolated_tl)}.")

    # Example code snippet to round the values to 5 decimal places
    interpolated_sa1 = round(float(interpolated_sa1), 5)
    interpolated_sa02 = round(float(interpolated_sa02), 5)
    interpolated_tl = round(float(interpolated_tl), 5)
    Favalue = round(float(Favalue), 5)
    Fvvalue = round(float(Fvvalue), 5)
    SMS = round(float(SMS), 5)
    SM1 = round(float(SM1), 5)
    SDS = round(float(SDS), 5)
    SD1 = round(float(SD1), 5)
    Ts = round(float(Ts), 5)
    To = round(float(To), 5)
    given_point = [round(lat, 5), round(lon, 5)]

    SDS_rounded = round(SDS * 10) / 10
    if SDS_rounded % 2 != 0:  # If it's not an even tenth
        SDS_rounded = np.ceil(SDS_rounded * 5) / 5  # Adjust to the next even tenth

    # If the adjustment leads to a value that is less than or equal to the original SDS,
    # increase it to the next even tenth above the original SDS
    if SDS_rounded <= SDS:
        SDS_rounded = np.ceil((SDS + 0.1) * 10) / 10


    # Title and labels
    if site != "F": 
        plt.title('Design Response Spectra')
        plt.xlabel('Period (T), s')
        plt.ylabel('Spectral Acceleration (g)')
        plt.ylim(0, SDS_rounded )
        plt.yticks([i * 0.2 for i in range(int(SDS_rounded / 0.2) + 2)])
        plt.xlim(0, 17)
        plt.xticks(range(18))
        plt.legend()
        plt.grid(True)
        buffer = BytesIO()
        plt.figtext(0.5, 0.5, "Data shown is an estimate and\nmay not reflect actual values.", ha='center', va='center',
                    fontsize=30, color='gray', alpha=0.3, rotation=30, weight='bold')
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    else:
        plt.close('all')  
        image_base64 = None
    

    # print("Interpolated Sa1:", interpolated_sa1)
    # print("Interpolated Sa0.2:", interpolated_sa02)
    # print("Interpolated TL:", interpolated_tl)
    # print("Fa value:", Favalue)
    # print("Fv value:", Fvvalue)
    # print("SMS:", SMS)
    # print("SM1:", SM1)
    # print("SDS:", SDS)
    # print("SD1:", SD1)
    # print("Ts:", Ts)
    # print("To:", To)



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
        'image_base64': image_base64,
    }




# lat = 10.1073
# lon = 123.1452
# site = "F"
# fainput = 0
# fvinput = 3
# process_sa_pga_map(lat, lon, site, fainput, fvinput)
