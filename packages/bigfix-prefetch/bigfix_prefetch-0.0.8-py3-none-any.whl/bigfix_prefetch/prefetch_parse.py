#!/usr/bin/env python
"""This script takes a bigfix prefetch and parses it into a hash dictionary

This is the opposite of:
- https://github.com/jgstew/generate_bes_from_template/blob/master/action_prefetch_from_template.py
"""

from __future__ import absolute_import

import re
import warnings


def parse_prefetch(prefetch):
    """parse bigfix prefetch using regex"""
    parsed_prefetch = {}
    parsed_prefetch['raw_prefetch'] = prefetch

    if "size:" in prefetch:
        # print("- prefetch statement:")
        # get file name:  /prefetch (\S+) /
        # get size:  / size:(\d+) /
        # get sha1:  / sha1:(\w{40}) /
        # get sha256:  / sha256:(\w{64})/
        # get url:  / (\S+://\S+)/
        parsed_prefetch['prefetch_type'] = "statement"
        parsed_prefetch['file_name'] = re.search(r'prefetch (\S+) ', prefetch).group(1)
        parsed_prefetch['file_size'] = re.search(r' size:(\d+) ', prefetch).group(1)
        parsed_prefetch['file_sha1'] = re.search(r' sha1:(\w+) ', prefetch).group(1)
        parsed_prefetch['download_url'] = re.search(r' (\S+://\S+)', prefetch).group(1)
        try:
            # NOTE: sha256 is technically optional, though now "mandatory" for some configs
            parsed_prefetch['file_sha256'] = re.search(r' sha256:(\w+)', prefetch).group(1)
        except AttributeError:
            warnings.warn("sha256 is missing which is valid unless enhanced security is enforced")
    if "size=" in prefetch:
        # print("- prefetch block:")
        # get file name:  / name=(\S+)/
        # get size:  / size=(\d+)/
        # get sha1:  / sha1=(\w{40})/
        # get sha256:  / sha256=(\w{64})/
        # get url:  / url=(\S+://\S+)/
        parsed_prefetch['prefetch_type'] = "block"
        parsed_prefetch['file_name'] = re.search(r' name=(\S+)', prefetch).group(1)
        parsed_prefetch['file_size'] = re.search(r' size=(\d+)', prefetch).group(1)
        try:
            # NOTE: sha1 is NOT required for prefetch blocks, but always expected
            parsed_prefetch['file_sha1'] = re.search(r' sha1=(\w+)', prefetch).group(1)
        except AttributeError:
            warnings.warn("prefetch block is missing sha1 which is unusual, but technically valid")
        parsed_prefetch['download_url'] = re.search(r' url=(\S+://\S+)', prefetch).group(1)
        try:
            # NOTE: sha256 is technically optional, though now "mandatory" for some configs
            parsed_prefetch['file_sha256'] = re.search(r' sha256=(\w+)', prefetch).group(1)
        except AttributeError:
            warnings.warn("sha256 is missing which is valid unless enhanced security is enforced")

    return parsed_prefetch


def main():
    """Only called if this script is run directly"""
    print(parse_prefetch("add prefetch item name=LGPO.zip \
sha1=0c74dac83aed569607aaa6df152206c709eef769 size=815660 \
url=https://download.microsoft.com/download/8/5/C/85C25433-A1B0-4FFA-9429-7E023E7DA8D8/LGPO.zip \
sha256=6ffb6416366652993c992280e29faea3507b5b5aa661c33ba1af31f48acea9c4"))
    print(parse_prefetch("prefetch unzip.exe sha1:e1652b058195db3f5f754b7ab430652ae04a50b8 \
size:167936 http://software.bigfix.com/download/redist/unzip-5.52.exe"))


# if called directly, then run this example:
if __name__ == '__main__':
    main()
