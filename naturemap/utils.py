import csv
from datetime import datetime
from django.contrib.gis.geos import GEOSGeometry
from .models import TaxonLocation


def import_naturemap_data(path='nmpspecies.csv'):
    f = open(path, 'r')
    reader = csv.reader(f)
    print(next(reader))
    count = 0
    then = datetime.now()
    print('Starting import of Naturemap data')
    new_records = []

    for row in reader:
        new_records.append(TaxonLocation(
            name=row[0],
            point=GEOSGeometry(row[1], srid=4283),
            supra=row[2],
            family=row[3],
            kingdom=row[4],
            conservation_status=row[5],
            vernacular=row[6],
            collector=row[7],
            collected_date=datetime.strptime(row[8], '%Y-%m-%d') if row[8] else None,
            survey=row[9],
            metadata={'source': row[10]},
            creator_id=1,  # Default value, assumes user with ID 1 exists.
            modifier_id=1,  # Default value, assumes user with ID 1 exists.
        ))
        count += 1
        if count % 1000 == 0:  # Commit our new records to the database.
            TaxonLocation.objects.bulk_create(new_records)  # bulk_create is WAY faster.
            new_records = []
            elapsed = (datetime.now() - then).microseconds
            print('Processed {} records, {} s/1000 records'.format(count, elapsed / 1000 / 1000))
            then = datetime.now()

    if new_records:  # Save any remaining records in our list.
        TaxonLocation.objects.bulk_create(new_records)
        new_records = []
