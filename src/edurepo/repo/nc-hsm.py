#!/usr/bin/env python

import json
import string
import sys


def find_statement_text(t):
    for l in j:
        if 'statement' in l and l['statement'] is not None and t in l['statement']:

            return l


def find_id(t):
    for l in j:
        if 'shortCode' in l and l['shortCode'] is not None and t in l['shortCode']:
            return l

raw_json = open('/home/trawick/git/standards-data/clean-data/CC/math/CC-math-0.8.0.json').read()
clean_json = ''
for b in raw_json:
    if ord(b) > 127:
        clean_json += '_'
    else:
        clean_json += b
clean_json = string.replace(clean_json, '&lt;sup&gt;___&lt;/sup&gt;', '')

j = json.loads(clean_json)

math_1_objectives = ['N-RN.1', 'N-RN.2', 'N-Q.1', 'N-Q.2', 'N-Q.3', 'A-SSE.1', 'A-SSE.2', 'A-SSE.3',
                     'A-APR.1', 'A-CED.1', 'A-CED.2', 'A-CED.3', 'A-CED.4', 'A-REI.1', 'A-REI.3',
                     'A-REI.5', 'A-REI.6', 'A-REI.10', 'A-REI.11', 'A-REI.12', 'F-IF.1', 'F-IF.2',
                     'F-IF.3', 'F-IF.4', 'F-IF.5', 'F-IF.6', 'F-IF.7', 'F-IF.8', 'F-IF.9',
                     'F-BF.1', 'F-BF.2', 'F-BF.3', 'F-LE.1', 'F-LE.2', 'F-LE.3', 'F-LE.5',
                     'G-CO.1', 'G-GPE.4', 'G-GPE.5', 'G-GPE.6', 'G-GPE.7', 'G-GMD.1', 'G-GMD.3',
                     'S-ID.1', 'S-ID.2', 'S-ID.3', 'S-ID.5', 'S-ID.6', 'S-ID.7', 'S-ID.8',
                     'S-ID.9', ]
math_1_code = 'NC-HSM-I'
math_1_desc = 'State of North Carolina High School Math I'

math_2_objectives = ['N-RN.2', 'N-Q.1', 'N-Q.2', 'N-Q.3', 'A-SSE.1', 'A-SSE.2', 'A-SSE.3',
                     'A-APR.1', 'A-APR.3', 'A-CED.1', 'A-CED.2', 'A-CED.3', 'A-CED.4', 'A-REI.1',
                     'A-REI.2', 'A-REI.4', 'A-REI.7', 'A-REI.10', 'A-REI.11', 'F-IF.2', 'F-IF.4',
                     'F-IF.7', 'F-IF.8', 'F-IF.9', 'F-BF.1', 'F-BF.3', 'G-CO.2', 'G-CO.3',
                     'G-CO.4', 'G-CO.5', 'G-CO.6', 'G-CO.7', 'G-CO.8', 'G-CO.10', 'G-CO.13',
                     'G-SRT.1', 'G-SRT.6', 'G-SRT.7', 'G-SRT.8', 'G-SRT.9', 'G-SRT.11',
                     'G-GPE.1', 'G-GPE.6', 'G-GMD.4', 'G-MG.1', 'G-MG.2', 'G-MG.3', 'S-IC.2',
                     'S-IC.6', 'S-CP.1', 'S-CP.2', 'S-CP.3', 'S-CP.4', 'S-CP.5', 'S-CP.6',
                     'S-CP.7', 'S-CP.8', 'S-CP.9', 'N-RN.3']
math_2_code = 'NC-HSM-II'
math_2_desc = 'State of North Carolina High School Math II'

math_3_objectives = ['N-RN.3', 'N-Q.1', 'N-Q.2', 'N-Q.3', 'N-CN.1', 'N-CN.2', 'N-CN.7',
                     'N-CN.9', 'A-SSE.1', 'A-SSE.2', 'A-SSE.3', 'A-SSE.4', 'A-APR.1',
                     'A-APR.2', 'A-APR.3', 'A-APR.4', 'A-APR.6', 'A-APR.7', 'A-CED.1',
                     'A-CED.2', 'A-CED.3', 'A-CED.4', 'A-REI.1', 'A-REI.2', 'A-REI.4',
                     'A-REI.10', 'A-REI.11', 'F-IF.2', 'F-IF.4', 'F-IF.5', 'F-IF.7',
                     'F-IF.8', 'F-IF.9', 'F-BF.1', 'F-BF.2', 'F-BF.3', 'F-BF.4',
                     'F-LE.3', 'F-LE.4', 'F-TF.1', 'F-TF.2', 'F-TF.5', 'F-TF.8',
                     'G-CO.1', 'G-CO.9', 'G-CO.10', 'G-CO.11', 'G-CO.12', 'G-SRT.2',
                     'G-SRT.3', 'G-SRT.4', 'G-SRT.5', 'G-C.1', 'G-C.2', 'G-C.3', 'G-C.5',
                     'G-GPE.1', 'G-GPE.2', 'G-MG.3', 'S-ID.4', 'S-IC.1', 'S-IC.3',
                     'S-IC.4', 'S-IC.5', 'S-IC.6', 'S-MD.6', 'S-MD.7']
math_3_code = 'NC-HSM-III'
math_3_desc = 'State of North Carolina High School Math III'

courses = [(math_1_objectives, math_1_code, math_1_desc),
           (math_2_objectives, math_2_code, math_3_desc),
           (math_3_objectives, math_3_code, math_3_desc)]

for cur in courses:
    f = cur[0]
    c = cur[1]
    d = cur[2]

    xmlf = open('%s.xml' % c, 'w')
    print >> xmlf, r"""<?xml version="1.0" encoding="utf-8"?>
<course-standard id="%s">
  <description>%s</description>
  <source>http://www.corestandards.org/assets/CCSSI_Math%%20Standards.pdf</source>
  <category>K12-M</category>
  <objectives>""" % (c, d)

    for line in f:
        line = line.decode('utf-8').strip()
        # print '"%s"' % line
        x = find_id(line)
        if x:
            # print x['code']
            # print x['statement'].encode('utf-8')
            statement = x['statement']
            print >> xmlf, r"""    <objective id="%s-%s">
      <description>%s</description>
    </objective>""" % (c, x['shortCode'], statement)
        else:
            print >> sys.stderr, '(not an id)'
        #x = find_statement_text(line)
        #if x:
            # print x['code']
            # print x['statement'].encode('utf-8')
        #    pass
        #else:
        #    pass
        #    # print '(not part of any objective statement)'

    print >> xmlf, """  </objectives>
</course-standard>"""
