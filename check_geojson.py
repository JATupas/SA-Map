import json

filepath = r'C:\Users\shade\ShadeApp\SA-Map\myapp\static\maps\ph_poi.geojson'

with open(filepath, encoding='utf-8') as f:
    data = json.load(f)

# Just show the first feature
if 'features' in data and len(data['features']) > 0:
    feature = data['features'][0]
    print(json.dumps(feature, indent=4))
else:
    print("No features found in the GeoJSON.")
