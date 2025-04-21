from django.core.management.base import BaseCommand
from myapp.models import POI
from shapely.geometry import shape
import ijson
import json
import decimal

BATCH_SIZE = 5000  # Adjust for performance balance

class Command(BaseCommand):
    help = "Efficiently import POIs from a large GeoJSON file and log skipped features"

    @staticmethod
    def convert_decimal(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def handle(self, *args, **kwargs):
        source_path = r"C:\Users\shade\ShadeApp\SA-Map\myapp\static\maps\ph_poi.geojson"
        skipped_path = r"C:\Users\shade\ShadeApp\SA-Map\myapp\static\maps\skipped_pois.geojson"

        print("🚀 Starting efficient POI import using `ijson` and `bulk_create`...")

        poi_batch = []
        skipped_features = []
        total = 0
        imported = 0
        skipped = 0

        with open(source_path, 'r', encoding='utf-8') as f:
            parser = ijson.items(f, "features.item")

            for i, feature in enumerate(parser, start=1):
                total += 1
                try:
                    props = feature.get("properties", {})
                    geom = feature.get("geometry")

                    if not geom:
                        raise ValueError("Missing geometry")

                    shapely_geom = shape(geom)

                    if geom["type"] != "Point":
                        centroid = shapely_geom.centroid
                        lon, lat = centroid.x, centroid.y
                    else:
                        lon, lat = geom["coordinates"]

                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                        raise ValueError("Invalid coordinates")

                    name = props.get("name") or props.get("official_name") or props.get("wikidata") or "Unnamed"

                    # Prepare POI object
                    poi = POI(name=name, latitude=lat, longitude=lon)
                    poi_batch.append(poi)

                except Exception as e:
                    skipped += 1
                    skipped_features.append(feature)
                    skip_name = feature.get("properties", {}).get("name", "Unnamed")
                    print(f"⚠️  Skipped #{i} — {skip_name} — Reason: {e}")

                # Bulk insert every batch
                if len(poi_batch) >= BATCH_SIZE:
                    POI.objects.bulk_create(poi_batch, ignore_conflicts=True)
                    imported += len(poi_batch)
                    print(f"📍 Imported {imported} POIs so far...")
                    poi_batch.clear()

            # Final flush
            if poi_batch:
                POI.objects.bulk_create(poi_batch, ignore_conflicts=True)
                imported += len(poi_batch)
                print(f"📍 Final batch imported. Total Imported: {imported}")

        # Save skipped features to a separate GeoJSON
        if skipped_features:
            with open(skipped_path, 'w', encoding='utf-8') as out_f:
                json.dump({
                    "type": "FeatureCollection",
                    "features": skipped_features
                }, out_f, indent=2, default=self.convert_decimal)

        print("✅ Import complete!")
        print(f"✅ Total Imported: {imported}")
        print(f"⚠️  Total Skipped: {skipped} (logged in skipped_pois.geojson)")
