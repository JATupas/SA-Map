import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.ops import unary_union
import geopandas as gpd
import ast
import matplotlib.pyplot as plt
import math
from scipy import stats
import os

# # file paths
# output_file_path = 'C:/Users/shade/Downloads/SHADE App/demos/Reccurence Model Calculator/GR1/'
# gr_file_path = 'C:/Users/shade/Downloads/SHADE App/demos/Reccurence Model Calculator/GR1/Graphs/'
# luzon_seismic_sources = 'C:/Users/shade/Downloads/SHADE App/demos/Reccurence Model Calculator/Luzon Seismic Sources.xlsx'

# # CSV of EQ events (Declustered or not)
# rawEQ = 'C:/Users/shade/Downloads/SHADE App/demos/Reccurence Model Calculator/Declustered.csv'
# # CSV of Fault parameters
# rawFaults = 'C:/Users/shade/Downloads/SHADE App/demos/Reccurence Model Calculator/Simple Fault Sources.xlsx'

def analyze_faults(output_file_path, gr_file_path, luzon_seismic_sources, rawEQ, rawFaults, Buffer_Size):

    rawEQ = pd.read_csv(rawEQ)
    rawFaults = pd.read_excel(rawFaults)

    def check_if_df(df):
        if isinstance(df, pd.DataFrame):
            return df
        else:
            raise ValueError("The instance is not a DataFrame. Terminating operation.")
    
    def add_coords_column(CAT):
        def concatenate_coordinates(row):
            return f"({row['longitude']}, {row['latitude']})"

        CAT['Coords'] = CAT.apply(concatenate_coordinates, axis=1)
        return CAT


    def convert_coords_to_list(coords_values_str):
        try:
            # Convert the string to a Python list using ast.literal_eval
            coordinates_list = ast.literal_eval(coords_values_str)

            return coordinates_list

        except (ValueError, SyntaxError) as e:
            # Handle exceptions, e.g., if the values in 'Coords' are not valid list literals
            print("Error:", e)
            return []


    def km_to_gps_degrees(kilometers, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        
        earth_circumference_at_equator_km = 40075.017  # Earth's circumference at the equator in kilometers
        # Calculate the distance in degrees of longitude at the given latitude
        degrees_per_km_longitude = 360 / earth_circumference_at_equator_km
        # Calculate the distance in degrees of latitude
        degrees_per_km_latitude = degrees_per_km_longitude / math.cos(math.radians(latitude))
        # Convert kilometers to GPS degrees
        gps_degrees = kilometers * degrees_per_km_latitude
        return gps_degrees


    def preprocess_dataframe(CAT):
        # Drop rows where TClass is not "Crustal"
        CAT = CAT[CAT['depth'] < 25]

        # Drop rows where EQ Event is 0
        CAT = CAT[CAT['EQ Event'] != 0]
        return CAT


    def buffering_and_gr(fault_name, EQCat, vertices, luzon_seismic_sources):

        vertices = check_if_df(vertices)

        def check_inside_polygon(row):
            point = Point(row['Longitude'], row['Latitude'])
            if point.within(polygon):
                return 1
            else:
                return 0
            
        def get_fault(array ,name):
            for item in array:
                if item["segment"] == name:
                    return item["maxmag"]
            return None
            
        condition = vertices['Name'] == fault_name

        current_fault_df = vertices[condition]

        luzon_dict = luzon_seismic_sources.to_dict('records')

        print(luzon_dict)

        fault_max_mag = get_fault(luzon_dict, fault_name)

        latitude = current_fault_df['latitude'].mean()

        kilometers = Buffer_Size

        x_coords = current_fault_df['longitude'].tolist()
        y_coords = current_fault_df['latitude'].tolist()

        current_fault_df = add_coords_column(current_fault_df)

        # Combine all values in the 'Coords' column into a single string
        coordinates_str = '[' + ', '.join(current_fault_df['Coords']) + ']'
        coordinates_set = convert_coords_to_list(coordinates_str)

        CAT = EQCat

        # Set all values in the renamed column to an empty string
        CAT['EQ Event'] = ''

        # Calculate the mean of the "LONGITUDE" column
        mean_x = current_fault_df['latitude'].mean()

        # Extract the coordinates from the DataFrame
        coordinates = [(row['longitude'], row['latitude'])
                    for _, row in current_fault_df.iterrows()]

        # Create a LineString object from the coordinates
        line = LineString(coordinates)

        buffer_distance = km_to_gps_degrees(kilometers, latitude)

        # Create a buffer around the line
        buffered_line = line.buffer(buffer_distance, resolution=50)

        if buffered_line.is_empty:
            print("Buffered line is empty. Adjust the buffer distance.")
        else:
            # Check if buffered_line is a MultiPolygon
            if isinstance(buffered_line, MultiPolygon):
                # If it's a MultiPolygon, handle it appropriately
                print("Buffered line is a MultiPolygon. Handling it appropriately.")
                # Convert MultiPolygon to list of Polygons
                polygon = [Polygon(polygon.exterior) for polygon in buffered_line]
            else:
                # If it's a single Polygon, directly create a Polygon object
                polygon = Polygon(buffered_line.exterior)
                # Further processing...

                # Extract the exterior coordinates of the buffered line
                buffered_coords = list(buffered_line.exterior.coords)

                # Extract x and y coordinates from the buffered_coords
                buffered_x_coords, buffered_y_coords = zip(*buffered_coords)
            

            # Apply the function to the DataFrame
            CAT['EQ Event'] = CAT.apply(check_inside_polygon, axis=1)

             # Plot the points inside the polygon in green and outside in red
            inside_points = CAT[CAT['EQ Event'] == 1]
            plt.scatter(inside_points['Longitude'], inside_points['Latitude'],
                        color='green', marker='o', label='Inside Polygon', alpha=0.5)

        CAT = preprocess_dataframe(CAT)

        # Display unique values and their counts for the EQ Event column
        eq_event_counts = CAT['EQ Event'].value_counts()
        print(eq_event_counts)

        static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
        ph_shapefile = os.path.join(static_folder, 'PHL_adm0.shp')
        gdf = gpd.read_file(ph_shapefile)



        # Plot the outline of the Philippines
        gdf.plot(edgecolor='black', color='white', figsize=(20, 16))

        # Plot the events
        plt.scatter(CAT['Longitude'], CAT['Latitude'], color='green', marker='x', alpha=0.25, s=5)
        plt.plot(x_coords, y_coords, color='purple', marker='o',
                linestyle=':', label='Line through Coordinates', linewidth=6)
        
        plt.scatter(x_coords, y_coords, color='blue',
                    marker='o', label='Coordinates', s=2)

        # Plot the polygon
        gCAT = gpd.GeoDataFrame(geometry=[polygon])
        ax = gCAT.plot(ax=plt.gca(), facecolor='none', edgecolor='blue')

        plt.title('Fault Location in PH Map')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.savefig(output_file_path+f'{fault_name}_' +'For_Area.png', bbox_inches='tight')
        plt.clf()

        # THIS PART IS FOR THE ZOOMED IN AREA PART

        # Create a scatter plot
        plt.figure(figsize=(20, 16))
        plt.scatter(x_coords, y_coords, color='blue',
                    marker='o', label='Coordinates')

        # Plot the events
        plt.scatter(CAT['Longitude'], CAT['Latitude'], color='green', marker='x')
        plt.plot(x_coords, y_coords, color='purple', marker='o',
                linestyle='-', label='Line through Coordinates', linewidth=6.5)

        # Plot the polygon
        gCAT = gpd.GeoDataFrame(geometry=[polygon])
        ax = gCAT.plot(ax=plt.gca(), facecolor='none', edgecolor='blue')

        plt.title('Events inside N-km radius of fault')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.savefig(output_file_path+f'{fault_name}_' +'For_Buffer.png', bbox_inches='tight')

        CAT.to_excel(output_file_path+f'{fault_name}_'+"For_Print.xlsx")

        if CAT.empty:
            print(f"No earthquake data inside buffer for fault '{fault_name}'. Skipping...")
            return None, None, None, None

        magnitudes = CAT['Magnitude']
        mag_hi = fault_max_mag if fault_max_mag is not None else np.max(magnitudes)
        mag_low = 4.0

        a, b = gutenberg_richter(magnitudes, fault_name)
        
        return a, b, mag_hi, mag_low


    def gutenberg_richter(magnitudes, fault_name):
        if len(magnitudes) <= 1:
            print(f"Not enough distinct data points for fault '{fault_name}'. Skipping...")
            return None, None

        elif len(np.unique(magnitudes)) == 1:
            print(f"All magnitude values are identical for fault '{fault_name}'. Skipping...")
            return None, None

        counts = np.zeros(magnitudes.shape[0])

        # Compute the number of events with magnitude M >= m
        for i, m in enumerate(magnitudes):
            counts[i] = np.sum(magnitudes >= m)

        # Normalize counts
        norm = np.sum(counts)
        counts_n = counts / norm

        # Filter by removing empty bins for the log plot
        counts_n_f = counts_n[counts_n != 0]
        magnitudes_f = magnitudes[counts_n != 0]

        # Compute linear regression
        reg = stats.linregress(magnitudes_f, np.log10(counts_n_f))

        fig, ax = plt.subplots()
        ax.plot(magnitudes_f, counts_n_f, 'o', mfc='cornflowerblue', mec='black')

        # Plot linear regression
        label = r'a = {:.2f} $\pm$ {:.2f}'.format(reg.intercept, reg.intercept_stderr) + '\n' + \
                r'b = {:.2f} $\pm$ {:.2f}'.format(reg.slope, reg.stderr)
        plt.plot(magnitudes_f, 10 ** (reg.intercept + reg.slope * magnitudes_f), 'crimson', label=label)

        ax.set_yscale('log')
        ax.set_xlabel('m', fontsize=14)
        ax.set_ylabel(r'normalized counts', fontsize=14)
        ax.set_title('Gutenberg–Richter law', fontsize=20, pad=20)
        plt.legend()
        plt.grid()
        plt.savefig(gr_file_path + f'{fault_name}' + '_gutenberg_richter.jpeg',
                    dpi=300, bbox_inches='tight')

        return reg.intercept, -reg.slope
    
    luzon_df = pd.read_excel(luzon_seismic_sources, sheet_name='simple')

    def get_unique_fault_names(rawFaults):
        """
        Retrieve unique fault names from rawFaults, which can be either a DataFrame or a file path.

        Parameters:
            rawFaults (str or pandas.DataFrame): Either a file path or a DataFrame containing fault data.

        Returns:
            list or None: A list of unique fault names if successfully retrieved, otherwise None.
        """
        # Check if 'rawFaults' is a DataFrame or a file path
        if isinstance(rawFaults, pd.DataFrame):
            # DataFrame is provided directly
            if 'Name' in rawFaults.columns and not rawFaults.empty:
                # Attempt to retrieve unique values from the 'Name' column
                try:
                    # Get unique values from the 'Name' column
                    faults = rawFaults['Name'].unique()
                    return faults.tolist() # Convert numpy array to list
                except Exception as e:
                    raise ValueError("Error occurred while retrieving unique fault names from DataFrame:", e)
                    
            else:
                raise ValueError("DataFrame 'rawFaults' does not contain the 'Name' column or is empty.")
                
        else:
            # rawFaults is a file path
            try:
                # Attempt to read the file into a DataFrame
                rawFaults_df = pd.read_excel(rawFaults)  # Assuming it's a CSV file, modify if necessary
                if 'Name' in rawFaults_df.columns and not rawFaults_df.empty:
                    # Attempt to retrieve unique values from the 'Name' column
                    try:
                        # Get unique values from the 'Name' column
                        faults = rawFaults_df['Name'].unique()
                        return faults.tolist()  # Convert numpy array to list
                    except Exception as e:
                        raise ValueError("Error occurred while retrieving unique fault names from DataFrame:", e)
                        
                else:
                    raise ValueError("DataFrame 'rawFaults_df' does not contain the 'Name' column or is empty.")
            except Exception as e:
                raise ValueError("Error occurred while reading the file:", e)

    # Example usage:
    faults = get_unique_fault_names(rawFaults)


    def gr_loop(faults, EQCat, vertices, luzon_seismic_sources):
        summary = pd.DataFrame(columns=["Fault Name", "a-value", "b-value", "Min Magnitude", "Max Magnitude", "Ocurrence"])

        for fault in faults:
            a, b, mag_hi, mag_low = buffering_and_gr(fault, EQCat, vertices, luzon_seismic_sources)
            print(f'completed gr for {fault}')

            # Check if there are enough data points for analysis
            if a is not None and b is not None:  # Check if a and b are not None (indicating enough data points)
                # Create a DataFrame for the current fault's statistics
                fault_data = pd.DataFrame({
                    "Fault Name": [fault],
                    "a-value": [a],
                    "b-value": [b],
                    "Min Magnitude": [mag_low],
                    "Max Magnitude": [mag_hi],
                    "Ocurrence": [(10 ** (a - b * mag_low) - 10 ** (a - b * mag_hi))/100]
                })

                # Concatenate the fault_data DataFrame to the summary DataFrame
                summary = pd.concat([summary, fault_data], ignore_index=True)

        # Save the updated "summary" DataFrame to an Excel file
        summary.to_excel(output_file_path + "Summary.xlsx", index=False)


    gr_loop(faults, rawEQ, rawFaults, luzon_df)

# analyze_faults(output_file_path, gr_file_path, luzon_seismic_sources, rawEQ, rawFaults, 20)