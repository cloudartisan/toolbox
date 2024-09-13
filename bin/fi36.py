#!/usr/bin/env python3

"""
Given a Falcon Instance name, computes its obfuscated hash.

The calculation involves taking an FNV hash, encoding in base 36, and
trimming to the first 6 characters.

Falcon subdomains contain the obfuscated hash. For example:
- aws-prod9-apnortheast1 becomes mchho0.svc.sfdcfc.net
- aws-prod5-uswest2 becomes lywfpd.svc.sfdcfc.net

Usage:
    $ python3 -m pip install fnvhash base36
    $ python3 fi_hash_36.py aws-prod9-apnortheast1
    mchho0
    $ python3 fi_hash_36.py aws-prod5-uswest2
    lywfpd

Python:
    from fi_hash_36 import fi_hash_36
    print(fi_hash_36("aws-prod9-apnortheast1")
"""

import sys
import os

import fnvhash
import base36


MAXINT32 = 2**31 - 1
MAXINT64 = 2**63 - 1
CHARLEN = 6


def fi_hash_36(fi: str) -> str:
    """
    Given a Falcon Instance name, returns its obfuscated hash.

    Converts the FI name to lowercase, computes the FNV hash, encodes in
    base 36, returns the first CHARLEN characters.
    """
    hash_code = (fnvhash.fnv1_64(fi.lower().encode()) & MAXINT32)
    return base36.dumps(hash_code)
    #hash_code = (fnvhash.fnv1_64(fi.lower().encode()) & MAXINT32) % MAXINT64
    #return base36.dumps(hash_code)[:CHARLEN]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <falcon_instance_name>".format(os.path.basename(sys.argv[0])))
        sys.exit(1)
    print(fi_hash_36(sys.argv[1]))
