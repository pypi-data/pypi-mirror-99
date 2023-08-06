#!/usr/bin/env python
"""This script takes a file path, optionally a URL, and generates
 a bigfix prefetch statement."""
# Related:
#  - https://github.com/jgstew/tools/blob/master/Python/url_to_prefetch.py
#  - https://bigfix.me/relevance/details/3022868

from __future__ import absolute_import

import os
from hashlib import sha1, sha256


def file_to_prefetch(file_path, url="http://unknown"):
    """Return the bigfix prefetch generated from the provided file. URL optional.
    This function only reads the file once but computes both hashes using chunks."""
    hashes = sha1(), sha256()
    chunk_size = max(4 * 1024, max(each_hash.block_size for each_hash in hashes))
    file_size = 0
    # changing spaces in file name to underscores due to prefetch issues without it
    #  alternatively, could download as sha1 and rename after
    file_name = os.path.basename(file_path).replace(' ', '_')

    if not(os.path.isfile(file_path) and os.access(file_path, os.R_OK)):
        return "Error: file does not exist or is not readable! " + file_path

    with open(file_path, 'rb') as file_object:
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break
            # NOTE: This is probably not needed, could read directly from filesystem
            file_size += len(chunk)
            for each_hash in hashes:
                each_hash.update(chunk)

    # print("Debug_Info:: file:" + file_path + " url:" + url + \
    #            " chunksize:" + str(chunk_size))
    # NOTE: this should probably return a hash so that the format can be handled elsewhere.
    return "prefetch %s sha1:%s size:%d %s sha256:%s" % \
                (file_name, hashes[0].hexdigest(), file_size, url, hashes[1].hexdigest())


def main(file_path="LICENSE"):
    """Only called if this script is run directly"""
    print(file_to_prefetch(file_path))


# if called directly, then run this example:
if __name__ == '__main__':
    main()
