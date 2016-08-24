#!/usr/bin/env python
"""
Checks JSON files for errors. Recursively scans current dir.

requires: demjson
"""

import os

import demjson

linter = demjson.jsonlint()

for root, dirs, files in os.walk('.'):
  for name in files:
    filename = os.path.join(root, name)
    if filename.endswith('.json'):
      #print(filename)
      linter.main([filename])
