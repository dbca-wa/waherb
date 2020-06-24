import csv
from datetime import datetime
from .models import Name


def import_wacensus():
    print('Creating Kingdoms')
    f = open('kingdoms.csv', 'r')
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        Name.objects.create(name=row[0], rank='Kingdom')

    print('Creating names')
    f = open('names.csv', 'r')
    reader = csv.reader(f)
    next(reader)
    count = 0
    then = datetime.now()

    for row in reader:
        count += 1
        try:
            Name.objects.create(name=row[0], rank=row[1], metadata={'kingdom': row[2]})
            if count % 1000 == 0:  # Commit our new records to the database.
                elapsed = (datetime.now() - then).seconds
                print('Processed {} records, {:.2f} sec/1000 records'.format(count, elapsed / (count / 1000)))
                then = datetime.now()
        except:
            print('Error: {}'.format(row))

    f = open('taxon_tree.csv', 'r')
    reader = csv.reader(f)
    next(reader)
    count = 0
    then = datetime.now()

    print('Generating taxon tree')
    # Disable MPTT updates, temporarily.
    with Name.objects.disable_mptt_updates():
        for row in reader:
            count += 1
            if row[0] != row[1]:
                name = Name.objects.get(name=row[0])
                name.parent = Name.objects.get(name=row[1])
                name.save()
                if count % 1000 == 0:  # Commit our new records to the database.
                    elapsed = (datetime.now() - then).seconds
                    print('Processed {} records, {:.2f} sec/1000 records'.format(count, elapsed / (count / 1000)))
                    then = datetime.now()

    Name.objects.rebuild()  # Rebuild the MPTT tree.
