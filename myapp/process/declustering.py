# DECLUSTERING SCRIPT

# Python utilities
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openquake.hmtk.seismicity.declusterer.dec_gardner_knopoff as gardner
import openquake.hmtk.seismicity.declusterer.dec_afteran as afteran_module
import openquake.hmtk.parsers.catalogue.csv_catalogue_parser as catalogue_parser
import openquake.hmtk.seismicity.declusterer.distance_time_windows as dt_windows

# Import HMTK I/O Tools
# from openquake.hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser, CsvCatalogueWriter


# HMTK Declustering Tools
# from openquake.hmtk.seismicity.declusterer.dec_afteran import Afteran
# from openquake.hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
# from openquake.hmtk.seismicity.declusterer.distance_time_windows import GardnerKnopoffWindow, UhrhammerWindow, GruenthalWindow
# ifile = "C:/Users/shade/Downloads/SHADE App/demos/Catalog Declustering Tool/Aegean_ExtendedCat1.csv"
# output = "C:/Users/shade/Downloads/SHADE App/demos/Catalog Declustering Tool/"
# Method = "Gardner-Knopoff"
# Time_Window = "Gardner-Knopoff"
def decluster_catalogue(ifile, output, Method, Time_Window):
    parser = catalogue_parser.CsvCatalogueParser(ifile)
    catalogue = parser.read_file()

    # for row in catalogue:
    #     print(row)

    gardner_knopoff = gardner.GardnerKnopoffType1()
    afteran_instance = afteran_module.Afteran()
    # vcl = 0
    # flag_vector = 0
    if Method == "Gardner-Knopoff":
        if Time_Window == "Gardner-Knopoff":
            declust_config = {'time_distance_window': dt_windows.GardnerKnopoffWindow(), 'fs_time_prop': 1.0}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = gardner_knopoff.decluster(catalogue, declust_config)
        elif Time_Window == "Urhammer":
            declust_config = {'time_distance_window': dt_windows.UhrhammerWindow(), 'fs_time_prop': 1.0}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = gardner_knopoff.decluster(catalogue, declust_config)
        elif Time_Window == "Gruenthal":
            declust_config = {'time_distance_window': dt_windows.GruenthalWindow(), 'fs_time_prop': 1.0}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = gardner_knopoff.decluster(catalogue, declust_config)
        else:
            print("Invalid Time Window")
    elif Method == "Afteran":
        if Time_Window == "Gardner-Knopoff":
            declust_config = {'time_distance_window': dt_windows.GardnerKnopoffWindow(), 'time_window': 100.}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = afteran_instance.decluster(catalogue, declust_config)
        elif Time_Window == "Urhammer":
            declust_config = {'time_distance_window': dt_windows.UhrhammerWindow(), 'time_window': 100.}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = afteran_instance.decluster(catalogue, declust_config)
        elif Time_Window == "Gruenthal":
            declust_config = {'time_distance_window': dt_windows.GruenthalWindow(), 'time_window': 100.}
            print(declust_config)
            print('Running declustering ...')
            vcl, flag_vector = afteran_instance.decluster(catalogue, declust_config)
        else:
            print("Invalid Time Window")
    else:
        print("Invalid Method")

    print('done!')
    data = np.column_stack([catalogue.data['year'], catalogue.data['month'], catalogue.data['day'], catalogue.data['hour'], catalogue.data['minute'],
                           catalogue.data['second'], catalogue.data['magnitude'], catalogue.data['depth'], catalogue.data['longitude'], catalogue.data['latitude'], vcl, flag_vector])


    print('%s clusters found' % np.max(vcl))
    print('%s Non-poissionian events identified' % np.sum(flag_vector != 0))

    declustered = {
        'Cluster No.': vcl,
        'Index': flag_vector
    }

    df = pd.DataFrame(data)

    df.to_csv(output + 'Declustered.csv', index=False, header=['Year', 'Month', 'Day', 'Hour',
              'Minute', 'Second', 'Magnitude', 'depth', 'Longitude', 'Latitude', 'Cluster No.', 'Index'])

# decluster_catalogue(ifile, output, Method, Time_Window)