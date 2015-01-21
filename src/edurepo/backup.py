import datetime
import gzip
import os
import sys

import django
from django.core.management import call_command


def usage():
    print >> sys.stderr, "Usage: %s backup-directory" % sys.argv[0]
    sys.exit(1)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edurepo.settings")
    django.setup()

    backup_dir = None
    try:
        backup_dir = sys.argv[1]
    except IndexError:
        usage()

    basename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M.json.gz')
    with gzip.open(os.path.join(backup_dir, basename), 'wb') as f:
        call_command('dumpdata', stdout=f, indent=2)

    files = []
    for basename in os.listdir(backup_dir):
        if '.json.gz' not in basename:
            print 'Unexpected file %s found...' % basename
            continue
        fullname = os.path.join(backup_dir, basename)
        files.append((fullname, os.stat(fullname).st_mtime))
    files = sorted(files, key=lambda file_plus_mtime: file_plus_mtime[1])

    older_files = files[:-10]
    for older_file in older_files:
        os.remove(older_file[0])

if __name__ == '__main__':
    main()
