import csv
from datetime import datetime
from django.contrib.gis.geos import Point
from .models import TaxonLocation


def import_naturemap_data(path='/var/www/archive/nmpspecies.csv'):
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
            point=Point((float(row[1]), float(row[2])), srid=4283),
            supra=row[3],
            family=row[4],
            kingdom=row[5],
            conservation_status=row[6],
            vernacular=row[7],
            collector=row[8],
            collected_date=datetime.strptime(row[9], '%d/%b/%y') if row[9] else None,
            survey=row[10],
            metadata={'source': row[11]},
            creator_id=1,  # Default value, assumes user with ID 1 exists.
            modifier_id=1,  # Default value, assumes user with ID 1 exists.
        ))
        count += 1
        if count % 1000 == 0:  # Commit our new records to the database.
            TaxonLocation.objects.bulk_create(new_records)  # bulk_create is WAY faster.
            new_records = []
            elapsed = (datetime.now() - then).microseconds
            print('Processed {} records, {} ms/1000 records'.format(count, elapsed))
            then = datetime.now()

    if new_records:  # Save any remaining records in our list.
        TaxonLocation.objects.bulk_create(new_records)
        new_records = []
