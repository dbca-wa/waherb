import csv
from datetime import datetime
from .models import Name, Reference


def import_wacensus():
    """This script assumes that you have kingdoms.csv, names.csv and taxon_tree.csv files
    in the project root.
    """
    print('Creating Kingdoms')
    f = open('kingdoms.csv', 'r')
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        Name.objects.create(name=row[0], rank='Kingdom')

    f = open('names.csv', 'r')
    reader = csv.reader(f)
    next(reader)
    count = 0
    then = datetime.now()
    print('Creating names')

    for row in reader:
        count += 1
        if not Name.objects.filter(name=row[0]).exists():
            Name.objects.create(name=row[0], rank=row[1], metadata={'kingdom': row[2], 'name_id': row[3]})
        if count % 1000 == 0:
            elapsed = (datetime.now() - then).seconds
            print('Processed {} records, {:.2f} sec/1000 records'.format(count, elapsed))
            then = datetime.now()

    f = open('taxon_tree.csv', 'r')
    reader = csv.reader(f)
    next(reader)
    count = 0
    then = datetime.now()
    updates = []

    print('Generating taxon tree')
    # Disable MPTT updates, temporarily.
    with Name.objects.disable_mptt_updates():
        for row in reader:
            count += 1
            if row[0] != row[1]:  # Disallow self as parent.
                name = Name.objects.get(name=row[0])
                name.parent = Name.objects.get(name=row[1])
                updates.append(name)
                if count % 1000 == 0:
                    Name.objects.bulk_update(updates, ['parent'])
                    updates = []
                    elapsed = (datetime.now() - then).seconds
                    print('Processed {} records, {:.2f} sec/1000 records'.format(count, elapsed))
                    then = datetime.now()

    if updates:
        Name.objects.bulk_update(updates, ['parent'])  # Final flush of the updates list.

    print('Rebuilding MPTT tree')
    Name.objects.rebuild()  # Rebuild the MPTT tree.

    """
    f = open('apni_names.csv', 'r')
    reader = csv.reader(f)
    next(reader)
    count = 0
    then = datetime.now()

    print('Importing APNI/NSL data')
    for row in reader:
        if Name.objects.filter(name=row[0]):
            count += 1
            name = Name.objects.get(name=row[0])
            #name.nsl_url = row[1]
            #name.metadata['author'] = row[2]
            #name.metadata['original_name'] = row[6]
            #name.save()
            ref, created = Reference.objects.get_or_create(title=row[3], nsl_url=row[7], metadata={'publish_year': row[4]})
            name.references.add(ref)
            if count % 1000 == 0:
                elapsed = (datetime.now() - then).seconds
                print('Processed {} records, {:.2f} sec/1000 records'.format(count, elapsed))
                then = datetime.now()
    """
