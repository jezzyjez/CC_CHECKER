#!/usr/bin/env python3
import re

class CommonFunc:
    def __init__(self):
        pass
    
    def parse_component(self, line):
        bcom_regex = re.compile("bcom\s+", re.IGNORECASE)
        fdb_regex = re.compile("fdb\s+|fdb_\w+|bdi_pub", re.IGNORECASE)
        if re.match(bcom_regex, line):
            return 'bcom'
        elif re.match(fdb_regex, line):
            return 'fdb'
        else:
            return None
