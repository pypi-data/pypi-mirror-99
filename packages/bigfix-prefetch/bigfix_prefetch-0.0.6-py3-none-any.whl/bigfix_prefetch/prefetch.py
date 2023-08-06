#!/usr/bin/env python
"""This script takes a bigfix prefetch and downloads the file

The downloaded file will be validated against the prefetch statement

This validates both the prefetch and the resulting file downloaded are still valid

Validation Steps: Size, SHA1, SHA256  (warn if sha256 is not present, but generate it)

This script accepts a prefetch statement, or prefetch block, or a dictionary with prefetch info
"""
# Related:
#  - https://github.com/jgstew/tools/blob/master/Python/url_to_prefetch.py

import sys
import site
import os.path
import warnings

# add the module path
site.addsitedir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bigfix_prefetch.prefetch_parse  # pylint: disable=import-error,wrong-import-position
import bigfix_prefetch.prefetch_from_url  # pylint: disable=import-error,wrong-import-position
import bigfix_prefetch.prefetches_have_matching_hashes  # pylint: disable=import-error,wrong-import-position
import bigfix_prefetch.prefetch_validate  # pylint: disable=import-error,wrong-import-position


def prefetch(prefetch_data, save_file=True):
    """actually prefetch the file and validate the file and prefetch data"""
    parsed_prefetch = {}
    file_path = None

    # make sure prefetch is valid first
    if not bigfix_prefetch.prefetch_validate(prefetch_data):
        warnings.warn("ERROR: bad prefetch")
        sys.exit(1)

    if 'file_size' in prefetch_data:
        parsed_prefetch = prefetch_data
    else:
        parsed_prefetch = bigfix_prefetch.prefetch_parse(prefetch_data)
    # NOTE: do the download & validation (url_to_prefetch)

    # if file_path doesn't exist, then use file_name and current directory
    #  if file doesn't exist, then download file there
    #  then validate it against prefetch data

    if save_file:
        if 'file_path' in parsed_prefetch:
            file_path = parsed_prefetch['file_path']
        else:
            file_path = parsed_prefetch['file_name']
        print(file_path)

    # regenerate the prefetch, then compare.
    test_prefetch = bigfix_prefetch.prefetch_from_url(
        parsed_prefetch['download_url'],
        True,
        file_path
    )

    print(test_prefetch)
    print(parsed_prefetch)

    # validate the hashes match
    return bigfix_prefetch.prefetches_have_matching_hashes(
        parsed_prefetch,
        test_prefetch
    )


def main():
    """Only called if prefetch is run directly"""
    prefetch_test = {
        'file_name': 'unzip.exe',
        'file_size': '167936',
        'file_sha1': 'e1652b058195db3f5f754b7ab430652ae04a50b8',
        'download_url': 'http://software.bigfix.com/download/redist/unzip-5.52.exe'
    }
    print(prefetch(prefetch_test, False))


# if called directly, then run this example:
if __name__ == '__main__':
    main()
