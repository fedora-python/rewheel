import argparse
import csv
import email.parser
import os
import io
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
    """Recreates a whee of package with given record_path and returns path
    to the newly created wheel."""
    site_dir = os.path.dirname(os.path.dirname(record_path))
    record_relpath = record_path[len(site_dir):].strip(os.path.sep)
    to_write, to_omit = get_records_to_pack(site_dir, record_relpath)
    new_wheel_name = get_wheel_name(record_path) + '.whl'

    new_wheel = zipfile.ZipFile(new_wheel_name, mode='w', compression=zipfile.ZIP_DEFLATED)
    # we need to write a new record with just the files that we will write,
    # e.g. not binaries and *.pyc/*.pyo files
    new_record = io.StringIO()
    writer = csv.writer(new_record)

    # handle files that we can write straight away
    for f, sha_hash, size in to_write:
        new_wheel.write(os.path.join(site_dir, f), arcname=f)
        writer.writerow([f, sha_hash,size])

    # rewrite the old wheel file with a new computed one
    writer.writerow([record_relpath, '', ''])
    new_wheel.writestr(record_relpath, new_record.getvalue())

    new_wheel.close()

    return new_wheel.filename

def get_wheel_name(record_path):
    """Return proper name of the wheel, without .whl."""
    wheel_info_path = os.path.join(os.path.dirname(record_path), 'WHEEL')
    wheel_info = email.parser.Parser().parsestr(open(wheel_info_path).read())
    metadata_path = os.path.join(os.path.dirname(record_path), 'METADATA')
    metadata = email.parser.Parser().parsestr(open(metadata_path).read())

    # construct name parts according to wheel spec
    distribution = metadata.get('Name')
    version = metadata.get('Version')
    build_tag = '' # nothing for now
    lang_tag = []
    for t in wheel_info.get_all('Tag'):
        lang_tag.append(t.split('-')[0])
    lang_tag = '.'.join(lang_tag)
    abi_tag, plat_tag = wheel_info.get('Tag').split('-')[1:3]
    # leave out build tag, if it is empty
    to_join = filter(None, [distribution, version, build_tag, lang_tag, abi_tag, plat_tag])
    return '-'.join(list(to_join))

def get_records_to_pack(site_dir, record_relpath):
    """Accepts path of sitedir and path of RECORD file relative to it.
    Returns two lists:
    - list of files that can be written to new RECORD straight away
    - list of files that shouldn't be written or need some processing
      (pyc and pyo files, scripts)
    """
    record_contents = open(os.path.join(site_dir, record_relpath)).read()
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
               spl[0] == record_relpath:
                to_omit.append(spl)
            else:
                to_write.append(spl)
        else:
            pass # bad RECORD or empty line
    return to_write, to_omit
