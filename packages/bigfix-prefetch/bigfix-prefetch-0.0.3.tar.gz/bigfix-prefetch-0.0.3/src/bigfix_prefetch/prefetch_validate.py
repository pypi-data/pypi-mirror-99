#!/usr/bin/env python
"""
This script takes a bigfix prefetch and validates it

BigFix Prefetches:
    - Must have size
        - int or int(string) greater than 0
    - Must have sha1 if prefetch statement, always expected (except-invalid-prefetch-statement)
        - prefetch blocks do NOT require SHA1 (warn-optional-missing)
        - string of exactly 40 characters - case insensitive
    - Must have sha256 to work with enhanced security (warn-optional-missing)
        - string of exactly 64 characters - case insensitive

If enhanced security is a requirement, then SHA256 warnings become exceptions

MD5 is never used, only provided for use with IOCs or similar weak validation
"""

import warnings
import site
import os.path

# add path this script is in
site.addsitedir(os.path.dirname(os.path.abspath(__file__)))

import prefetch_parse  # pylint: disable=import-error,wrong-import-position


def validate_prefetch(bigfix_prefetch, sha256_required=False):  # pylint: disable=too-many-return-statements,too-many-branches
    """Validate the BigFix Prefetch"""

    # prefetch must not be null, empty string, or falsey
    if not bigfix_prefetch:
        warnings.warn("ERROR: prefetch is empty or invalid")
        return False

    # if prefetch_one is not a dictionary, then parse it into one
    if 'file_size' in bigfix_prefetch:
        parsed_bigfix_prefetch = bigfix_prefetch
        if 'raw_prefetch' not in parsed_bigfix_prefetch:
            # adding a raw_prefetch value for later warnings
            parsed_bigfix_prefetch['raw_prefetch'] = "NOTE: \
                source was a prefetch dictionary already"
    else:
        try:
            parsed_bigfix_prefetch = prefetch_parse.parse_prefetch(bigfix_prefetch)
        except AttributeError:
            warnings.warn("ERROR: prefetch is invalid, could not be parsed\n" + bigfix_prefetch)
            return False

    # if file_sha1 is present, it must be exactly 40 characters
    if 'file_sha1' in parsed_bigfix_prefetch and len(parsed_bigfix_prefetch['file_sha1']) != 40:
        warnings.warn("ERROR: sha1 not the correct length(40)")
        return False

    # if files_sha256 is present, it must be exactly 64 characters
    if 'file_sha256' in parsed_bigfix_prefetch and len(parsed_bigfix_prefetch['file_sha256']) != 64:
        warnings.warn("ERROR: sha256 not the correct length(64)")
        return False

    # file_size must be present
    if 'file_size' not in parsed_bigfix_prefetch:
        warnings.warn("ERROR: prefetch size is missing\n" + parsed_bigfix_prefetch['raw_prefetch'])
        return False

    # file size must be >= 0
    if int(parsed_bigfix_prefetch['file_size']) <= 0:
        warnings.warn("ERROR: prefetch size is invalid\n" + parsed_bigfix_prefetch['raw_prefetch'])
        return False

    # if sha256 is required but missing, then invalid
    if 'file_sha256' not in parsed_bigfix_prefetch:
        if not sha256_required:
            warnings.warn("INFO: \
                sha256 is recommended, but missing. Please add it for future requirements.")
        else:
            warnings.warn("ERROR: \
                sha256 is missing but required\n" + parsed_bigfix_prefetch['raw_prefetch'])
            return False

    # if a prefetch statement, then sha1 MUST be present
    if ('prefetch_type' in parsed_bigfix_prefetch
            and parsed_bigfix_prefetch['prefetch_type'] == 'statement'):
        print("Info: prefetech statement")
        if 'file_sha1' not in parsed_bigfix_prefetch:
            warnings.warn("ERROR: sha1 is mandatory in prefetch statement but missing")
            return False

    # future: validate the characters within the hash strings [a-fA-F0-9]
    # future: validate the characters within the name and URL

    return True


def main():
    """Only called if this script is run directly"""
    prefetch_dictionary_valid = {
        'file_name': 'unzip.exe',
        'file_size': '167936',
        'file_sha1': 'e1652b058195db3f5f754b7ab430652ae04a50b8',
        'file_sha256': '8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a',

        'download_url': 'http://software.bigfix.com/download/redist/unzip-5.52.exe'
    }
    print(validate_prefetch(prefetch_dictionary_valid))
    # pylint: disable=line-too-long
    print(validate_prefetch("add prefetch item name=unzip.exe sha256=8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a size=167936 url=http://software.bigfix.com/download/redist/unzip-5.52.exe"))
    print(validate_prefetch("add prefetch item name=unzip.exe sha256=8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a size=0 url=http://software.bigfix.com/download/redist/unzip-5.52.exe"))
    print(validate_prefetch("add prefetch item name=unzip.exe sha256=8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a size=ABC url=http://software.bigfix.com/download/redist/unzip-5.52.exe"))


# if called directly, then run this example:
if __name__ == '__main__':
    main()
