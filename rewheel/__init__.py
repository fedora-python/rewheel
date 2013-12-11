import argparse
import os
import sys
import zipfile

def run():
    parser = argparse.ArgumentParser(description='Recreate wheel of package with given RECORD.')
    parser.add_argument('record', help='Path to RECORD file')

    ns = parser.parse_args()
    retcode = 0
    try:
        print(rewheel_from_record(vars(ns)['record']))
    except BaseException as e:
        print('Failed: {}'.format(e))
        retcode = 1
    sys.exit(1)

def rewheel_from_record(record_path):
    record_contents = open(record_path).read()
    recfiles = get_records_to_pack(record_contents)
    site_dir = os.path.dirname(os.path.dirname(record_path))
    new_wheel = zipfile.ZipFile('foo.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    for f, sha_hash, size in recfiles:
        new_wheel.write(os.path.join(site_dir, f), arcname=f)
    new_wheel.close()
    return new_wheel.filename

def get_records_to_pack(record_contents):
    lines = []
    for l in record_contents.splitlines():
        spl = l.split(',')
        if len(spl) == 3:
            # ignore abs paths (binaries) and pyc+pyo files
            if not os.path.isabs(spl[0]) and \
               not spl[0].endswith('.pyc') and \
               not spl[0].endswith('.pyo'):
                lines.append(spl)
        else:
            pass # bad RECORD or empty line
    return lines
