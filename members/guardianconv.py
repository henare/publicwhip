#!/usr/bin/python2.3
# $Id: guardianconv.py,v 1.2 2004/02/25 15:48:55 frabcus Exp $

# Converts tab file of Guardian URLs into XML

# The Public Whip, Copyright (C) 2003 Francis Irving and Julian Todd
# This is free software, and you are welcome to redistribute it under
# certain conditions.  However, it comes with ABSOLUTELY NO WARRANTY.
# For details see the file LICENSE.html in the top level of the source.

input = '../rawdata/mpinfo/guardian-mpsurls.txt'
date = '2004-02-25'

import sys
import string
sys.path.append("../pyscraper")
from resolvemembernames import memberList

print '''<?xml version="1.0" encoding="ISO-8859-1"?>
<publicwhip>'''

ih = open(input, 'r')

c = 0
for l in ih:
    c = c + 1
    origname, origcons, personurl, consurl = map(string.strip, l.split("\t"))
    id, name, cons =  memberList.matchfullnamecons(origname, origcons, date)
    print '<memberinfo id="%s" guardian_mp_summary="%s" />' % (id, personurl)
    print '<consinfo id="%s" guardian_election_results="%s" />' % (id, consurl)

assert c == 659, "Expected %d MPs" % c

ih.close()

print '</publicwhip>'
