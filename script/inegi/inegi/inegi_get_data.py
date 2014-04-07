#!/usr/bin/env python

import argparse
import os
import sys
import zipfile

try:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoSectionError, NoOptionError

import requests

def main():
    # Options for command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-download', help='Skip download files from source.',
                        action='store_true')
    parser.add_argument('-i', action='store_true',
                        help='Request confirmation before attempting to remove each file')
    parser.add_argument('-c', '--config',
                        help='Specify which config file to read.')
    parser.add_argument('directory',
                        help='Create necessary local directory hierarchy.')
    args = parser.parse_args()

    # Try to read the source configuration
    config = ConfigParser()
    try:
        if args.config:
            inegi_fp = args.config
        else:
            inegi_cfg = os.path.abspath(os.path.dirname(__file__))
            inegi_fp = os.path.join(inegi_cfg, 'inegi.cfg')
        config.readfp(open(inegi_fp))
    except IOError:
        print('Improperly configured.')
        sys.exit()

    chunk_size = 1024

    try:
        base_path = config.get('general', 'base_path')
    except NoSectionError, NoOptionError:
        print('Improperly configured.')
        sys.exit()

    # dir_path represents the directory where we store the downloaded files
    dir_path = args.directory

    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path, 0755)
        except OSError:
            print('Directory cannot be created.')
            sys.exit()

    os.chdir(dir_path)

    # Download all files listed on [entities] section
    if not args.skip_download:
        print('Downloading info from source...')

        try:
            entities = config.items('entities')
        except NoSectionError:
            print('Improperly configured.')
            sys.exit()

        for entity, url in entities:
            target_url = "".join([base_path, url])
            target_file = "".join([entity, '.zip'])

            if os.path.isfile(target_file) and args.i:
                message = 'Do you want to replace the file {0}: (y/n) '.format(target_file)
                replace = raw_input(message).lower()
                while replace != 'y' and replace != 'n':
                    replace = raw_input(message).lower()

                if replace == 'n':
                    continue

            r = requests.get(target_url, stream=True)

            if r.status_code == 200:
                with open(target_file, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size):
                        fd.write(chunk)

                if zipfile.is_zipfile(target_file):
                    if not os.path.isdir(entity):
                        os.mkdir(entity, 0755)

                    with zipfile.ZipFile(target_file) as zf:
                        zf.extractall(entity)
    else:
        print('Download skipped.')

if __name__ == '__main__':
    main()
