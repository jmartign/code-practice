#!/usr/bin/env python

from collections import Counter
import re


ip_regex = re.compile('(?:\d{1,3}\.){3}\d{1,3}')

def parse_line(line): 
    if line:
        m = ip_regex.search(line)
        if m:
            return m.group(0)
    return None

if __name__ == '__main__':
    in_file = 'auth.log'
    cnt = Counter()
    for line in open(in_file):
        ip = parse_line(line)
        if ip:
            cnt[ip] += 1
    for ip, c in cnt.most_common():
        print ip, c

