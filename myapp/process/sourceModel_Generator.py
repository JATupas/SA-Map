import pandas as pd

# File paths
# fault_file_path = 'C:/Users/shade/Downloads/drive-download-20231113T014254Z-001/Luzon Seismic Sources.xlsx'
# eq_file_path = 'C:/Users/shade/Downloads/drive-download-20231113T014254Z-001/DEC_Summary.xlsx'
# vertice_file_path = 'C:/Users/shade/Downloads/drive-download-20231113T014254Z-001/Simple Fault Sources VERTICES.xlsx'
# text_file_path = 'C:/Users/shade/Downloads/test.txt'

def create_model(text_file_path, fault_file_path, eq_file_path, vertice_file_path):
    # Open the text file in append and read-write mode
    text_file = open(text_file_path, "w")

    # Load the Excel file into a DataFrame
    df = pd.read_excel(fault_file_path)
    eq = pd.read_excel(eq_file_path)
    vr = pd.read_excel(vertice_file_path)

    text_file.writelines("<?xml version='1.0' encoding='utf-8'?>" + '\n')
    text_file.writelines('<nrml xmlns:gml="http://www.opengis.net/gml"' + '\n')
    text_file.writelines('\t' + 'xmlns="http://openquake.org/xmlns/nrml/0.4">' + '\n\n')
    text_file.writelines('\t' + '<sourceModel name="Final_PSHA 2016 Philippines_011517">' + '\n\n\n')

    fault_info_list = []

    def extract_fault_info(df, eq, vr, text_file):
        for index, (df_row, eq_row) in enumerate(zip(df.iterrows(), eq.iterrows())):
            df_index, df_row_data = df_row
            eq_index, eq_row_data = eq_row

            ocr_array = []
            vertices = vr[vr['Segment'] == df_row_data['segment']]

            coordinate_string = ""

            x_coords = vertices['xcoord'].tolist()
            y_coords = vertices['ycoord'].tolist()

            for i in range(0, int(eq_row_data['Bins'])):
                if eq_row_data[f'OCR_{i}'] != 0:
                    ocr_array.append(eq_row_data[f'OCR_{i}'])

            for i in range(0, len(vertices)):
                coordinate_string += f'{x_coords[i]} {y_coords[i]} \n'

            ocr_string = " ".join(str(r) for r in ocr_array)

            fault_info = {
                "FAULT ID": index + 1,  # Use the current iteration as the ID
                "FAULT NAME": df_row_data["segment"],
                "DIP": df_row_data["dip"],
                "A-VAL": eq_row_data["a-value"],
                "B-VAL": eq_row_data["b-value"],
                "MAX-MAG": eq_row_data["Max Magnitude"],
                "RAKE": df_row_data["rake"],
                "FAULT VERTICES": coordinate_string,  # Empty list for vertices
                "OCR": ocr_string  # Empty list for OCR values
            }

            text_file.writelines("\t" + f'<simpleFaultSource id="{index +1}" name="{df_row_data["segment"]}" tectonicRegion="Active Shallow Crust">' + '\n')
            text_file.writelines("\t\t" + "<simpleFaultGeometry>"+ '\n')
            text_file.writelines("\t\t\t" + "<gml:LineString>"+ '\n')
            text_file.writelines("\t\t\t\t" + "<gml:posList>"+ '\n')
            text_file.writelines({coordinate_string})
            text_file.writelines("\t\t\t\t" + "</gml:posList>"+ '\n')
            text_file.writelines("\t\t\t" + "</gml:LineString>"+ '\n')
            text_file.writelines("\t\t\t" + f'<dip>{df_row_data["dip"]}</dip>'+ '\n')
            text_file.writelines("\t\t\t" + "<upperSeismoDepth>5.0</upperSeismoDepth>"+ '\n')
            text_file.writelines("\t\t\t" + "<lowerSeismoDepth>28.0</lowerSeismoDepth>"+ '\n')
            text_file.writelines("\t\t" + "</simpleFaultGeometry>"+ '\n')
            text_file.writelines("\t\t" + "<magScaleRel>WC1994</magScaleRel>"+ '\n')
            text_file.writelines("\t\t" + "<ruptAspectRatio>1.0</ruptAspectRatio>"+ '\n')
            text_file.writelines("\t\t" + "<!-- -->"+ '\n')
            text_file.writelines("\t\t\t" + f'<incrementalMFD minMag="5.5" binWidth="0.1">' + '\n')
            text_file.writelines("\t\t" + f'<occurRates>{ocr_string}</occurRates>' + '\n')
            text_file.writelines("\t\t\t" + "</incrementalMFD>"+ '\n')
            text_file.writelines("\t\t\t" + "<!-- -->"+ '\n')
            text_file.writelines("\t\t\t" + "<!-- -"+ '\n')
            text_file.writelines("\t\t\t" + f'<truncGutenbergRichterMFD aValue="{eq_row_data["a-value"]}" bValue="{eq_row_data["b-value"]}" minMag="4.0" maxMag="{df_row_data["maxmag"]}" />' + '\n')
            text_file.writelines("\t\t\t" + "<!- -->"+ '\n')
            text_file.writelines("\t\t" + f'<rake>{df_row_data["rake"]}</rake>' + '\n')
            text_file.writelines("\t" + '</simpleFaultSource>' + "\n\n")

            fault_info_list.append(fault_info)

        return fault_info_list

    # Assuming you have 'df' and 'eq' DataFrames with the relevant columns
    # Call the function to extract fault_info
    fault_info_list = extract_fault_info(df, eq, vr, text_file)

    # You can then use the 'fault_info_list' as needed, combining information from both DataFrames.
    text_file.writelines('\t' + "</sourceModel>" + '\n')
    text_file.writelines('</nrml>' + '\n')
    print("Done!")

# create_model(text_file_path, fault_file_path, eq_file_path, vertice_file_path)