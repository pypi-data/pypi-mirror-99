#!/usr/bin/env python
"""
This script takes 2 prefetch statements, blocks, or dictionaries and validates they "match"

BigFix Prefetch Comparison:
    - Must have matching size
    - Must have at least one hash in common (sha1 or sha256)
    - All common hashes must match
    - SHA256 must be present and matching for enhanced security (optional-warn-missing)

If enhanced security is a requirement, then SHA256 warnings become exceptions
"""

import warnings

import site
import os.path

# add the module path
site.addsitedir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bigfix_prefetch.prefetch_parse  # pylint: disable=import-error,wrong-import-position
import bigfix_prefetch.prefetch_validate  # pylint: disable=import-error,wrong-import-position


def prefetches_have_matching_hashes(prefetch_one, prefetch_two, sha256_required=False):  # pylint: disable=too-many-branches,too-many-return-statements
    """Compare the file size and hashes to make sure they match"""
    hash_comparison_pass = {
        "sha256": None,
        "sha1": None,
    }

    # ensure both prefetches have the required details
    if not (
            bigfix_prefetch.prefetch_validate(prefetch_one)
            and bigfix_prefetch.prefetch_validate(prefetch_two)
    ):
        warnings.warn("ERROR: one or more prefetches are invalid")
        return False

    # if prefetch_one is not a dictionary, then parse it into one
    if 'file_size' in prefetch_one:
        parsed_prefetch_one = prefetch_one
    else:
        parsed_prefetch_one = bigfix_prefetch.prefetch_parse(prefetch_one)

    # if prefetch_two is not a dictionary, then parse it into one
    if 'file_size' in prefetch_two:
        parsed_prefetch_two = prefetch_two
    else:
        parsed_prefetch_two = bigfix_prefetch.prefetch_parse(prefetch_two)

    # Validate that file_size matches
    try:
        if int(parsed_prefetch_one['file_size']) != int(parsed_prefetch_two['file_size']):
            warnings.warn("ERROR: file_size does not match")
            return False
    except ValueError:
        warnings.warn("ERROR: Invalid file_size")
        return False

    # check if file_sha256 is present
    if (
            ("file_sha256" in parsed_prefetch_one)
            and ("file_sha256" in parsed_prefetch_two)
    ):
        # check if file_sha256 matches
        if parsed_prefetch_one['file_sha256'] != parsed_prefetch_two['file_sha256']:  # pylint: disable=no-else-return
            warnings.warn("ERROR: file_sha256 does not match")
            return False
        else:
            hash_comparison_pass["sha256"] = True
    else:
        # sha256 is not present, check if required:
        if sha256_required:
            warnings.warn("ERROR: file_sha256 does not match")
            return False

    # check if file_sha1 is present
    if (
            ("file_sha1" in parsed_prefetch_one)
            and ("file_sha1" in parsed_prefetch_two)
    ):
        # check file_sha1 matches
        if parsed_prefetch_one['file_sha1'] != parsed_prefetch_two['file_sha1']:  # pylint: disable=no-else-return
            warnings.warn("ERROR: SHA1 does not match")
            return False
        else:
            hash_comparison_pass["sha1"] = True
    else:
        # file_sha1 is missing - valid only for prefetch blocks
        warnings.warn("Warning: at least one prefetch missing SHA1")

    # verify at least 1 hash has passed comparison
    for key in hash_comparison_pass:
        if hash_comparison_pass[key] is True:
            return True

    # catch all:
    return False


def main():
    """Only called if this script is run directly"""
    prefetch_dictionary_one = {
        'file_name': 'unzip.exe',
        'file_size': '167936',

        'file_sha1': 'e1652b058195db3f5f754b7ab430652ae04a50b8',
        'file_sha256': '8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a',
        'download_url': 'http://software.bigfix.com/download/redist/unzip-5.52.exe'
    }
    print(
        prefetches_have_matching_hashes(prefetch_dictionary_one, prefetch_dictionary_one)
    )


# if called directly, then run this example:
if __name__ == '__main__':
    main()
