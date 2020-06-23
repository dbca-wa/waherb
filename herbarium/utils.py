import json
from datetime import datetime
from .models import TexpressData


def import_texpress_data(path='/var/www/archive/texpress_json_rows.txt'):
    """Utility function to import Texpress data from the flat file output.
    """
    f = open(path)
    count = 0
    then = datetime.now()
    print('Starting import of Texpress data')
    new_records = []

    for line in f.readlines():
        new_records.append(TexpressData(row=json.loads(line), row_text=line))
        count += 1
        if count % 1000 == 0:  # Commit our new records to the database.
            TexpressData.objects.bulk_create(new_records)
            new_records = []
            elapsed = (datetime.now() - then).seconds
            print('Processed {} records, {:.2f} s/1000 records'.format(count, elapsed / (count / 1000)))


def sanitise_data():
    """Utility function to clean up imported Texpress data.
    """
    count = 0
    then = datetime.now()
    print('Starting sanitise')

    for tex in TexpressData.objects.iterator():  # Use iterator() or we'll be OOM.
        # Merge multi-element string fields into a single string:
        if 'vegetati' in tex.row and isinstance(tex.row['vegetati'], list):
            tex.row['vegetati'] = ' '.join([i for i in tex.row['vegetati'] if i])
        if 'plantdes' in tex.row and isinstance(tex.row['plantdes'], list):
            tex.row['plantdes'] = ' '.join([i for i in tex.row['plantdes'] if i])
        if 'sitedesc' in tex.row and isinstance(tex.row['sitedesc'], list):
            tex.row['sitedesc'] = ' '.join([i for i in tex.row['sitedesc'] if i])
        if 'locality' in tex.row and isinstance(tex.row['locality'], list):
            tex.row['locality'] = ' '.join([i for i in tex.row['locality'] if i])
        if 'voucher' in tex.row and isinstance(tex.row['voucher'], list):
            tex.row['voucher'] = ' '.join([i for i in tex.row['voucher'] if i])
        if 'fre' in tex.row and isinstance(tex.row['fre'], list):
            tex.row['fre'] = ' '.join([i for i in tex.row['fre'] if i])
        # Convert single-element arrays into just that element value.
        for key, val in tex.row.items():
            if isinstance(val, list) and len(val) == 1:
                tex.row[key] = val[0]
        # Save JSON data into the indexed row_text field.
        tex.row_text = str(tex.row)
        tex.save()

        count += 1
        if count % 1000 == 0:
            elapsed = (datetime.now() - then).seconds
            print('Processed {} records, {:.2f} s/1000 records'.format(count, elapsed / (count / 1000)))
