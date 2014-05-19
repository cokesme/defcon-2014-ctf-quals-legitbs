#!/usr/bin/env pypy

# Print every IPv4 address in the same format as the torrent
# First try used python3 before I realized pypy would be way faster before I
# realized C/C++ would be fastest and also really easy to write
# mal <mal@sec.gd>

for a in range(0,256):
    for b in range(0,256):
        for c in range(0,256):
            for d in range(0,256):
                print str(a) + "." + str(b) + "." + str(c) + "." + str(d)

