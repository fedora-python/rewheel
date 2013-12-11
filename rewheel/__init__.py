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
    site_dir = os.path.dirname(os.path.dirname(record_path))
    record_relpath = record_path[len(site_dir):].strip(os.path.sep)
    to_write, to_omit = get_records_to_pack(record_contents, record_relpath)

    new_wheel = zipfile.ZipFile('foo.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    # we need to write a new record with just the files that we will write,
    # e.g. not binaries and *.pyc/*.pyo files
    new_record_lines = []
    for f, sha_hash, size in to_write:
        new_wheel.write(os.path.join(site_dir, f), arcname=f)
        new_record_lines.append(','.join([f, sha_hash,size]))

    # rewrite the old wheel file with a new computed one
    new_wheel.writestr(record_relpath, '\n'.join(new_record_lines))

    new_wheel.close()

    return new_wheel.filename

def get_records_to_pack(record_contents, record_relpath):
    to_write = []
    to_omit = []
    for l in record_contents.splitlines():
        spl = l.split(',')
        if len(spl) == 3:
            # new record will omit (or write differently):
            # - abs paths, paths with ".." (entry points),
            # - pyc+pyo files
            # - the old RECORD file
            # TODO: is there any better way to recognize an entry point?
            if os.path.isabs(spl[0]) or spl[0].startswith('..') or \
               spl[0].endswith('.pyc') or spl[0].endswith('.pyo') or \
               spl[0] != record_relpath:
                to_omit.append(spl)
            else:
                to_write.append(spl)
        else:
            pass # bad RECORD or empty line
    return to_write, to_omit
