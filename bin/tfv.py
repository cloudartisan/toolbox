#!/usr/bin/env python

import os
import hcl


def get_tf_required_version(path):
    for root, subdirs, files in os.walk(path):
        tf_files = [ os.path.join(root, f) for f in files if f.endswith('.tf') ]
        for tf in tf_files:
            with open(tf, 'r') as fp:
                try:
                    obj = hcl.load(fp)
                    if obj.has_key('terraform'):
                        return obj['terraform'].get('required_version', None)
                except Exception, e:
                    sys.stderr.write("Unable to parse %s\n" % tf)
    return None


if __name__ == '__main__':
    import sys
    print get_tf_required_version(os.path.abspath(sys.argv[1]))
